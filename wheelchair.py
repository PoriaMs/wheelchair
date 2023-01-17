# -*- coding: utf-8 -*-
import os
import subprocess
import sys
import fileinput
import click


def run_cmd(cmd):
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    while p.poll() is None:
        line = p.stdout.readline().strip()
        if line:
            print(str(line, "utf-8"))
        sys.stdout.flush()
        sys.stderr.flush()


def create(article_name):
    run_cmd("hugo new posts/" + article_name + "/index.md")
    name = "content/posts/" + article_name + "/index.md"
    for line in fileinput.input(name, inplace=1):
        line = line.replace("Index", article_name)
        print(line, end="")


def debug():
    run_cmd("hugo server -D -e production")


def publish():
    run_cmd("hugo")
    os.chdir("public")
    run_cmd("git add .")
    run_cmd("git commit -m \"updating site on $(date)\"")
    run_cmd("git push origin main")
    os.chdir("../")


def update():
    run_cmd("git submodule update --remote --merge")


@click.command()
@click.option('-d', is_flag=True, help='本地调试预览')
@click.option('-c', type=str, help='创建新文章')
@click.option('-p', is_flag=True, help='发表文章')
@click.option('-u', is_flag=True, help='升级主题')
def start(d, c, p, u):
    if d:
        debug()
    if c:
        create(c)
    if p:
        publish()
    if u:
        update()


if __name__ == "__main__":
    start()

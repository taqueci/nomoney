#!/bin/sh

echo "Setting Git configurations..."
git config --global core.autocrlf false
git config --global core.ignorecase false
git config core.quotepath false
git config merge.ff false
git config pull.rebase true
git config push.default simple

name=`git config user.name`
echo -n "Enter full name (e.g. Steven Tyler) [$name]: "
read name
test -z "$name" || git config --global user.name "$name"

email=`git config user.email`
echo -n "Enter e-mail address [$email]: "
read email
test -z "$email" || git config --global user.email "$email"

echo "Completed!"

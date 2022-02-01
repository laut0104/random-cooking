# ランダムクッキング

Random cooking is a web application that randomly recommends from the registered menus.

Technologies used:
- JQuery
- sqlite3

## DEMO

You can learn how to use this application by watching the video at this URL<"https://www.youtube.com/watch?v=qTpRze6oxZM">.

## How to use

First, enter the user information and register the user.Log in with your registered user name and password.You can browse the list of registered recipes on the screen after logging in.
Register ingredients, quantity, recipe, etc. on the recipe registration screen.You can jump to the recipe details page by clicking the recipe name on the recipe list screen.
The menu is recommended by pressing the button at the bottom of the recipe list screen.If you press the button again, the menu will be recommended at random again.
Then you can jump to the details page of the menu by pressing the enter button.

## Note

When entering the ingredients and the procedure for making, be careful not to enter the character string "/  /" because it will cause unintended behavior.

## Description
The images used in this Web application are stored in the images folder of the static folder, and css is stored directly under static.
It is application.py that handles database related data and its data. Basically, it consists of one html per page. apology.html is a page that is called when an error such as a user's input error occurs.
The database consists of two tables, a user table and a menu table.**I am using sqlite3 as a database.**You can change your password on the Setting page.You can log out on the Logout page.


## デモ
このURL<"https://www.youtube.com/watch?v=qTpRze6oxZM">の動画でデモンストレーションをやっていて使い方を学ぶことができます．

## 使い方
使い方の説明は以下の通りです．
1. まず，ユーザ情報としてユーザ名とパスワードを登録して，利用できるユーザを作成します．
2. 作成したユーザ名とパスワードでログインします．ログインしたら表示される画面がレシピ一覧画面です．
3. レシピ登録画面で食材とその食材の分量，作り方の手順などを登録してレシピを登録します．
4. レシピ一覧画面ではレシピのタイトルをクリックすることでその料理名の詳細画面に飛ぶことができます．
5. そして，**このWebアプリケーションの重要な機能であるメニュー推薦機能はメニュー決定ボタンを押すことで推薦してくれます．**
6. そして，もう一度ボタンを押すともう一度登録しているレシピからランダムで選んでくれます．
7. 決定ボタンを押すとそのメニューの詳細ページに飛ぶことができます．
8. Settingページでパスワードを変更することができます．
9. Logoutページでログアウトすることができます．

## 注意
レシピ登録画面で食材や分量，作り方の手順などを登録する際に("/  /")の文字列を入力してしまうと意図していない挙動となってしまうため，入力しないようにする必要がある．

## 概要
staticフォルダのimagesフォルダにはこのWebアプリケーションで使用している画像が格納されていて，cssはstatic直下に格納されてます．
データベース関連やそのデータを扱っているのはapplication.pyです．基本1ページにつき1つのhtmlで構成されている．apology.htmlはユーザの入力ミスなどのエラーが起こったときに呼び出されるページである．
データベースはユーザテーブルとメニューテーブルの2つのテーブルで構成されている．**データベースはsqlite3を使用している．**

### Author

- Miyu Yano
- miyuyano0104@gmail.com




## Шаг 1
Для начала укажем ссылку на репозиторий находящийся на нашем компьютере
```
pc@DESKTOP-11QI9NS MINGW64 ~
$ cd C:/Repositories/Rep_for_python
```
Для инициализации репозитория используем команду `git init`
```
pc@DESKTOP-11QI9NS MINGW64 /c/Repositories/Rep_for_python
$ git init
Initialized empty Git repository in C:/Repositories/Rep_for_python/.git/
pc@DESKTOP-11QI9NS MINGW64 /c/Repositories/Rep_for_python (master)
$ ls -la
total 4
drwxr-xr-x 1 pc 197121 0 Dec 11 20:24 ./
drwxr-xr-x 1 pc 197121 0 Dec 11 20:11 ../
drwxr-xr-x 1 pc 197121 0 Dec 11 20:24 .git/
```
Для просмотра статуса репозитория используем `git status`

```
pc@DESKTOP-11QI9NS MINGW64 /c/Repositories/Rep_for_python (master)
$ git status
On branch master

No commits yet

nothing to commit (create/copy files and use "git add" to track)
```
# Шаг 2
Создадим файл readme.txt при помощи `touch`
```
pc@DESKTOP-11QI9NS MINGW64 /c/Repositories/Rep_for_python (master)
$ touch readme.txt
```
Затем внесем в него изменения при помощи `nano`
```
pc@DESKTOP-11QI9NS MINGW64 /c/Repositories/Rep_for_python (master)
$ nano readme.txt
```
Но файл еще не отслеживается поэтому при вызове `git status`
```
pc@DESKTOP-11QI9NS MINGW64 /c/Repositories/Rep_for_python (master)
$ git status
On branch master

No commits yet

Untracked files:
  (use "git add <file>..." to include in what will be committed)
        readme.txt

nothing added to commit but untracked files present (use "git add" to track)
```
Добавим readme в репозиторий чтобы его отслеживать 
```
pc@DESKTOP-11QI9NS MINGW64 /c/Repositories/Rep_for_python (master)
$ git add readme.txt
warning: in the working copy of 'readme.txt', LF will be replaced by CRLF the next time Git touches it
```
Теперь 
```
pc@DESKTOP-11QI9NS MINGW64 /c/Repositories/Rep_for_python (master)
$ git status
On branch master

No commits yet

Changes to be committed:
  (use "git rm --cached <file>..." to unstage)
        new file:   readme.txt
```
Для совершения коммита необходимо задать своё имя и почту
```
pc@DESKTOP-11QI9NS MINGW64 /c/Repositories/Rep_for_python (master)
$ git config --global user.email "platonpotemkin51@gmail.com"

pc@DESKTOP-11QI9NS MINGW64 /c/Repositories/Rep_for_python (master)
$ git config --global user.name "Platon Potemkin"
```
```
pc@DESKTOP-11QI9NS MINGW64 /c/Repositories/Rep_for_python (master)
$ git commit -m "First files"
[master (root-commit) 875967e] First files
 1 file changed, 1 insertion(+)
 create mode 100644 readme.txt
```
Теперь при вызове `status`:
```
pc@DESKTOP-11QI9NS MINGW64 /c/Repositories/Rep_for_python (master)
$ git status
On branch master
nothing to commit, working tree clean
```
Для просмотра коммитов `git log`
```
pc@DESKTOP-11QI9NS MINGW64 /c/Repositories/Rep_for_python (master)
$ git log
commit 875967efa3e7cb48e1246fcfe8e97c3691495d1d (HEAD -> master)
Author: Platon Potemkin <platonpotemkin51@gmail.com>
Date:   Thu Dec 11 20:40:04 2025 +0300

    First files
```
# Шаг 3
Создадим в проводнике в соответсвующей папке репозитория readme_new.txt
```
pc@DESKTOP-11QI9NS MINGW64 /c/Repositories/Rep_for_python (master)
$ git status
On branch master
Untracked files:
  (use "git add <file>..." to include in what will be committed)
        readme_new.txt

nothing added to commit but untracked files present (use "git add" to track)
```
Добавим этот файл при помощи маски(добавляющей все текстовые файлы)
```
pc@DESKTOP-11QI9NS MINGW64 /c/Repositories/Rep_for_python (master)
$ git add '*.txt'
warning: in the working copy of 'readme.txt', LF will be replaced by CRLF the next time Git touches it
```
```
pc@DESKTOP-11QI9NS MINGW64 /c/Repositories/Rep_for_python (master)
$ git status
On branch master
Changes to be committed:
  (use "git restore --staged <file>..." to unstage)
        modified:   readme.txt
        new file:   readme_new.txt
```
И закоммитим
```
pc@DESKTOP-11QI9NS MINGW64 /c/Repositories/Rep_for_python (master)
$ git commit -m "Update readme and create readme_new"
[master f791995] Update readme and create readme_new
 2 files changed, 1 insertion(+), 1 deletion(-)
 create mode 100644 readme_new.txt
```
```
pc@DESKTOP-11QI9NS MINGW64 /c/Repositories/Rep_for_python (master)
$ git log
commit f7919952c653e8dd85529ff065986205fda36bb1 (HEAD -> master)
Author: Platon Potemkin <platonpotemkin51@gmail.com>
Date:   Thu Dec 11 20:49:20 2025 +0300

    Update readme and create readme_new

commit 875967efa3e7cb48e1246fcfe8e97c3691495d1d
Author: Platon Potemkin <platonpotemkin51@gmail.com>
Date:   Thu Dec 11 20:40:04 2025 +0300

    First files
```
# Шаг 4
Подключаем репозиторий из `github.com`
```
pc@DESKTOP-11QI9NS MINGW64 /c/Repositories/Rep_for_python (master)
$ git remote add origin https://github.com/platonpotemkin51-source/first_git.git
```
Устанавливаем связь между локальной веткой master и веткой master на удалённом сервере (origin)

Для этого потребуется создать ключ в настройках github
```
pc@DESKTOP-11QI9NS MINGW64 /c/Repositories/Rep_for_python (master)
$ git push -u origin master
Enumerating objects: 7, done.
Counting objects: 100% (7/7), done.
Delta compression using up to 16 threads
Compressing objects: 100% (3/3), done.
Writing objects: 100% (7/7), 510 bytes | 510.00 KiB/s, done.
Total 7 (delta 0), reused 0 (delta 0), pack-reused 0 (from 0)
To https://github.com/platonpotemkin51-source/first_git.git
 * [new branch]      master -> master
branch 'master' set up to track 'origin/master'.
```
Добавим две строки в readme.txt через удаленный репозиторий 

И обновим данные в локальной сети через `git pull origin master`
```
pc@DESKTOP-11QI9NS MINGW64 /c/Repositories/Rep_for_python (master)
$ git pull origin master
remote: Enumerating objects: 5, done.
remote: Counting objects: 100% (5/5), done.
remote: Compressing objects: 100% (3/3), done.
remote: Total 3 (delta 0), reused 0 (delta 0), pack-reused 0 (from 0)
Unpacking objects: 100% (3/3), 978 bytes | 61.00 KiB/s, done.
From https://github.com/platonpotemkin51-source/first_git
 * branch            master     -> FETCH_HEAD
   f791995..9bbd67c  master     -> origin/master
Updating f791995..9bbd67c
Fast-forward
 readme.txt | 2 ++
 1 file changed, 2 insertions(+)
```
Посмотрим теперь последние изменения `git diff HEAD`
```
pc@DESKTOP-11QI9NS MINGW64 /c/Repositories/Rep_for_python (master)
$ git diff HEAD
```
но изменений после коммита не было

Теперь добавим  строку в readme
```
pc@DESKTOP-11QI9NS MINGW64 /c/Repositories/Rep_for_python (master)
$ git diff HEAD
diff --git a/readme.txt b/readme.txt
index 825a90d..4980020 100644
--- a/readme.txt
+++ b/readme.txt
@@ -1,3 +1,4 @@
 Hello, world!
 hp_qQihUxaMwDFOw8cDyVLN8ZUHaolJLc0tFvnH
 gp_qQihUxaMwDFOw8cDyVLN8ZUHaolJLc0tFvnH
+_______________________________________
\ No newline at end of file
```
Также можем вернуть состояние ветки до последнего коммита через `git checkout -- readme.txt`
```
pc@DESKTOP-11QI9NS MINGW64 /c/Repositories/Rep_for_python (master)
$ git status
On branch master
Your branch is up to date with 'origin/master'.

Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
        modified:   readme.txt

Untracked files:
  (use "git add <file>..." to include in what will be committed)
        folder/

no changes added to commit (use "git add" and/or "git commit -a")

pc@DESKTOP-11QI9NS MINGW64 /c/Repositories/Rep_for_python (master)
$ git checkout -- readme.txt

```
Создадим папку `folder/`
```
pc@DESKTOP-11QI9NS MINGW64 /c/Repositories/Rep_for_python (master)
$ git status
On branch master
Your branch is up to date with 'origin/master'.

Untracked files:
  (use "git add <file>..." to include in what will be committed)
        folder/

nothing added to commit but untracked files present (use "git add" to track)
```
Также можем использовать `cat readme.txt` для просмотра содержимого
```
pc@DESKTOP-11QI9NS MINGW64 /c/Repositories/Rep_for_python (master)
$ cat readme.txt
Hello, world!
hp_qQihUxaMwDFOw8cDyVLN8ZUHaolJLc0tFvnH
gp_qQihUxaMwDFOw8cDyVLN8ZUHaolJLc0tFvnH
```
# Шаг 5

Создадим новую ветку `git branch clean_up` и перейдем в неё `git checkout clean_up`
```
pc@DESKTOP-11QI9NS MINGW64 /c/Repositories/Rep_for_python (master)
$ git branch clean_up

pc@DESKTOP-11QI9NS MINGW64 /c/Repositories/Rep_for_python (master)
$ git branch
  clean_up
* master

pc@DESKTOP-11QI9NS MINGW64 /c/Repositories/Rep_for_python (master)
$ git checkout clean_up
Switched to branch 'clean_up'

pc@DESKTOP-11QI9NS MINGW64 /c/Repositories/Rep_for_python (clean_up)
$ git branch
* clean_up
  master
```
Посмотрим содержимое ветки 
```
pc@DESKTOP-11QI9NS MINGW64 /c/Repositories/Rep_for_python (clean_up)
$ ls
folder/  readme.txt  readme_new.txt
```
Удалим папку `folder` и закоммитим это действие
```
pc@DESKTOP-11QI9NS MINGW64 /c/Repositories/Rep_for_python (clean_up)
$ rm -r folder

pc@DESKTOP-11QI9NS MINGW64 /c/Repositories/Rep_for_python (clean_up)
$ git commit -m 'Deleted folder'
On branch clean_up
nothing to commit, working tree clean
```
Также удалим `readme_new.txt` в статусе такой файл отображается в `deleted:    readme_new.txt`

И закоммитим действие 
```
pc@DESKTOP-11QI9NS MINGW64 /c/Repositories/Rep_for_python (clean_up)
$ git rm readme_new.txt
rm 'readme_new.txt'

pc@DESKTOP-11QI9NS MINGW64 /c/Repositories/Rep_for_python (clean_up)
$ git status
On branch clean_up
Changes to be committed:
  (use "git restore --staged <file>..." to unstage)
        deleted:    readme_new.txt


pc@DESKTOP-11QI9NS MINGW64 /c/Repositories/Rep_for_python (clean_up)
$ git commit -m 'Deleted readme_new'
[clean_up f9fcce0] Deleted readme_new
 1 file changed, 0 insertions(+), 0 deletions(-)
 delete mode 100644 readme_new.txt
```
Перейдем в ветку `master`
```
pc@DESKTOP-11QI9NS MINGW64 /c/Repositories/Rep_for_python (clean_up)
$ git checkout master
Switched to branch 'master'
Your branch is up to date with 'origin/master'.

pc@DESKTOP-11QI9NS MINGW64 /c/Repositories/Rep_for_python (master)
$ git branch
  clean_up
* master
```
Затем выполним слияние веток
```
pc@DESKTOP-11QI9NS MINGW64 /c/Repositories/Rep_for_python (master)
$ git merge clean_up
Updating 9bbd67c..f9fcce0
Fast-forward
 readme_new.txt | 0
 1 file changed, 0 insertions(+), 0 deletions(-)
 delete mode 100644 readme_new.txt
```
Теперь удалим ветку `clean_up`

```
pc@DESKTOP-11QI9NS MINGW64 /c/Repositories/Rep_for_python (master)
$ git branch -d clean_up
Deleted branch clean_up (was f9fcce0).
```
# Шаг 6 
Загружаем все на удаленный (github) репозиторий
```
pc@DESKTOP-11QI9NS MINGW64 /c/Repositories/Rep_for_python (master)
$ git push
Enumerating objects: 3, done.
Counting objects: 100% (3/3), done.
Delta compression using up to 16 threads
Compressing objects: 100% (1/1), done.
Writing objects: 100% (2/2), 246 bytes | 246.00 KiB/s, done.
Total 2 (delta 0), reused 0 (delta 0), pack-reused 0 (from 0)
To https://github.com/platonpotemkin51-source/first_git.git
   9bbd67c..f9fcce0  master -> master
```
## Что касается `GitHub Desktop`
GitHub Desktop значительно упрощает работу с Git для большинства повседневных задач, но для сложных операций все же потребуется знание командной строки.

#### Работа с репозиториями
- **Клонирование репозитория:** Простой интерфейс для клонирования с GitHub
- **Создание нового репозитория:** Локального или сразу с публикацией на GitHub
- **Добавление существующего репозитория:** Поддержка локальных проектов

Пример: Создание репозитория и первый коммит
```
1. File → New Repository
2. Указание имени, описания, пути
3. Автоматическое создание начального коммита
4. Публикация на GitHub 
```

#### Основные операции
**1. Commit (коммит):**
- Просмотр (изменений) для каждого файла
- Написание commit message с подсказками

**2. Push (отправка на сервер):**
- Автоматическая синхронизация после коммита 
- Кнопка "Push origin" для явной отправки

**3. Pull/Fetch (получение изменений):**
- Кнопка "Fetch origin" для проверки обновлений
- "Pull origin" для получения и слияния изменений
- Визуальное отображение расхождений с удаленным репозиторием

**4. Branch (ветвление):**
- Создание новой ветки в один клик
- Переключение между ветками
- Управление ветками (удаление, переименование)

Пример: Работа с ветками
```
1. Текущая ветка: main
2. Branch → New Branch (feature/new-feature)
3. Внесение изменений в файлы
4. Commit к новой ветке
5. Branch → Merge into current branch
```

**5. Merge (слияние):**
- Визуальное слияние веток
- Разрешение конфликтов через встроенный редактор

Пример 3: Разрешение конфликтов
```
1. При попытке слияния - обнаружен конфликт
2. GitHub Desktop показывает файлы с конфликтами
3. Открытие встроенного редактора
4. Визуальный выбор нужных изменений
5. Mark as resolved → Commit merge
```

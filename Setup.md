Generate ssh key:
```
ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
```
Copy the contents of the file ~/.ssh/id_rsa.pub to your SSH keys in your GitHub account settings.
Test SSH key:
```
ssh -T git@github.com
clone the repo:
git clone git://github.com/username/your-repository
```
Now cd to your git clone folder and do:
```
git remote set-url origin git@github.com:username/your-repository.git
```
Now try editing a file (try the README) and then do:

```
git pull
git add -A
git status
git commit -m "Update message"
git push
```

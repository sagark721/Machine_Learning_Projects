# Machine_Learning_Project
This repository is created for practice purpose to learn end to end Machine Learning Project 

## Accounts:

1. [Github](https://github.com/sagark721)
2. [Heroku](https://dashboard.heroku.com/account)

## Create Conda Environment:

```
conda create -p venv_test python==3.7 -y
```
> Note: -p is used so that the environment will be created in project folder. otherwise -n is used which would create folder in 'C' drive.




### Activate conda environment:
```
conda activate venv_test/
```


### Create requirements.txt file and install requirements using:
```
pip install -r requirements.txt
```

### Git Commands:
1. To add specific files into git:
```
    git add <file name 1> <file name 2>
```

2. To add all the file in the directory to git:
```
    git add .
```
> Note: if dont want to add some files, add their name in .gitignore file

3. If file is created and not added by git, following command will give the status /warning of files which were not added/tracked by git

```
    git status
```

4. To create a new version:
```
    git commit -m <"Message" (why are you creating this version)>
```

5. To check all versions maintained by git:
```
    git log
```

6. To send the version/changes to github:
```
git push origin main
```
> Note: here 'origin' is the variable,in which the remote url is stored (url which we copied during cloning)

7. To check the remote url:
```
git remote -v
```

8. To check branch:
```
git branch 
```
# Machine_Learning_Projects
#### This repository is created for practice purpose to learn end to end Machine Learning Project 

### Accounts:

1. [Github](https://github.com/sagark721)
2. [Heroku](https://dashboard.heroku.com/account)

Creating Conda Environment

```
conda create -p venv_test python==3.7 -y
```
(-p is used so that the environment will be created in project folder. otherwise -n is used which would create folden in 'C' drive.)




Activating conda environment:
```
conda activate venv_test/
```


create requirements.txt file and install requirements using:
```
pip install -r requirements.txt
```

## Notes:
1. To add specific files into git:
```
    git add <file name 1> <file name 2>
```

2. To add all the file in the directory to git:
```
    git add .
```

    - if dont want to add some files, add their name in .gitignore file

if file is created and not added by git, following command will give the status /warning of files which were not added/tracked by git

```
git status
```


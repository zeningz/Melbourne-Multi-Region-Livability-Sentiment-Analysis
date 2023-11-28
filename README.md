# Melbourne-Multi-Region-Livability-Sentiment-Analysis
# Team mumber:
    Wei Ge - 1074198
    Han Wang - 1041260 
    YanBei Jiang - 1087029
    Yiwen Zhang - 1002781
    Zening Zhang - 1078374
# Project Overview
Melbourne is one of the most famous cities in the world. Melbourne was the world's most liveable city for eight years in a row. However, in 2012, Melbourne is “only” ninth. Although it is a good ranking, some problems may happen in Melbourne. Twitter is one of the most popular social applications. There are many people in Melbourne who use Twitter. 
In this project, we will develop a cloud based solution to analyze twitter data from multiple perspectives.. This application is deployed on Unimelb Research Cloud(MRC).

# Ansible-playbook:
1. - Make sure you have at least 4 instances available and at least 400GB disk space on MRC 
2. - Replace the file “unimelb-COMP90024-2022-grp-3-openrc.sh” with your own MRC configuration file by downloading it on the MRC homepage
3. - Modify the ansible configuration file at ./ansible/host_vars/nectar.yaml 
    This file contains all the configuration information about setting up the system. There are a few configuration parameters that MUST be modified.
4. - Generate your own MRC private key as shown below and save it to your own computer, change the field ssh_private_key_path to your own private key path
5. - ou might change the volume mount or number of instances created if you have a larger capacity.
6. - Run the following command
    ```sudo ./launch_instance.sh```
    ```sudo ./install_dependency.sh```
    ```sudo ./deploy.sh```
# directory structure
```
  /ansible
  /backend
  /crawler
  /data_analysis
  /frontend
  /map_reduce
```

# Videos
- https://youtu.be/dki5nmgq5hg

# Website
Please visit our website at http://172.26.133.159:3000/

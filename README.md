# Momo Risk Control System Static Rule Engine

### about us
Website: https://security.immomo.com

WeChat:<br>
<img src="https://momo-mmsrc.oss-cn-hangzhou.aliyuncs.com/img-1c96a083-7392-3b72-8aec-bad201a6abab.jpeg" width="200" hegiht="200" align=center /><br>

[Project Introduction](https://mp.weixin.qq.com/s/quk43WU3Vg9cQmub06Azqg)

### Architecture Introduction

   ![风控系统架构图](./www/static/img/wiki/architecture.jpg)

The main branch of this project only supports Python3, and currently passed the Python 3.7.3 version test. If you need the python2.7 version, please use the tag: last-support-Python2.7 code.
### Quick Start
1. This project depends on redis, mysql, mongodb, so you need to prepare the environment and change the configuration items
```bash
    # For simplicity, you can use docker installation
    # docker installation document address (Take ubuntu as an example): https://docs.docker.com/install/linux/docker-ce/ubuntu/
    mongo: docker run -d --name mongo -v $HOME/docker_volumes/mongodb:/data/db  -p 27017:27017 mongo:latest
    mysql: docker run -d --name mysql -e MYSQL_ROOT_PASSWORD=root -v $HOME/docker_volumes/mysql:/var/lib/mysql -v $HOME/docker_volumes/conf/mysql:/etc/mysql/conf.d -p 3306:3306 mysql:5.6
    redis: docker run -d --name redis -p 6379:6379  -v $HOME/docker_volumes/redis:/var/lib/redis redis:latest
```

2. Create risk_control library in mysql
```bash
    docker exec -it mysql mysql -h 127.0.0.1 -u root -p # You need to enter a password later. If you install mysql in the above way, the password is root.
     CREATE DATABASE risk_control CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci ; # Specify the encoding format when creating the database to avoid garbled problems (note: this encoding format may have compatibility issues on lower versions of mysql) 
```
3. Install the required dependencies. This project is based on python3.7. You can run pip install -r requirements.txt to install the dependencies.
4. Initialize the tables needed for Django to run and create an account, and some data can be pre-generated (optional)
```bash
    # Under the www directory
    python manage.py makemigrations && python manage.py migrate
     # Create administrator account See other operations here-add users
     python manage.py createsuperuser # Enter the user name, password, and email address in order to create an administrator account
     # If you want to have an intuitive feel for the system, you can use the following instructions to pre-inject some data
     python manage.py init_risk_data 
```
5. Start service
```bash
    # Start the service process, manage the background, and intercept the log consumption process in nohup mode under aswan
     bash start.sh
```

### Backstage introduction

1. List management

    Provides basic data management capabilities for list-based policies.

    The dimensions of the list data include: user ID, IP, device number, payment account number, and mobile phone number. Later, you can expand other dimensions according to your needs.

    The list contains three types: black, white, gray list

    The list must belong to a certain item (used to determine the scope of the list), and items can be added in list management-list item management.

    ![名单管理](./www/static/img/wiki/menu.png)

2. List strategy

    The descriptor is {parameter name: single choice, assuming "user ID"} {opcode: on / off} {XX item: single choice, optional global} {dimension: single choice} {direction: black / white / Greylist}

    Example: User ID is in the user blacklist of the initial project

    ![List strategy](./www/static/img/wiki/menu_strategy.png)

3. Boolean strategy

    A boolean that does not pass a threshold. The descriptor is {parameter name: single choice, assuming "account ID"} {opcode: yes / no} {built-in function: abnormal user} Example: account ID is an abnormal user

    Pass threshold Boolean, the descriptor is {parameter name: single choice, assuming "account ID"} {opcode: greater than / less than / equal / not equal} {built-in function: historical login times} {threshold: 170} Example : Account ID history login times greater than 100

    ![Boolean strategy](./www/static/img/wiki/bool_strategy.png)

    What is a Built-in functions ? It is a custom logic judgment function that only needs to meet the requirements to return a Boolean value. For example, whether the registration time is within a certain range, and whether the current device is a commonly used device.

4. Time-frequency-controlled strategy

   The descriptor is the same {counting dimension: single choice, assuming "device"} to limit {threshold: integer N} times within {time period: time span} Example of an action : limit the operation to the same device 10 times a day. But how do I know How many times already? This needs to be reported. For details, please refer to Article 9 Data Source Management.

    ![Time-time frequency control strategy](./www/static/img/wiki/freq_strategy.png)

5. User-limited number-based policy

    Descriptors are the same {Counting Dimension: Single Choice, Assuming "Device"} Limit {Threshold: Integer N} users within {Time period: Time span}

    Example: Limited to 10 users on the same device. This strategy also requires data to be reported, and because it is related to the user, the reported data must include the user_id field (which needs to be configured in the data source). For details, see Article 9 Data Source Management

    ![User-limited number-based policy](./www/static/img/wiki/user_strategy.png)

6. Rule management

    Control atom: The control action after hitting a certain policy, such as intercepting ... The policy atoms described in 2--5 above are combined according to priority, and executed from top to bottom, until a policy is hit, the corresponding response is returned. Governance atom of strategy. This module is more re-interactive, completing the configuration, combination, weighting, etc. of the strategy
    ![Rule configuration page](./www/static/img/wiki/rule_manage.png)

7. Log management

    The logs of all hit policies are displayed here, and audit-related logs will also be included `The next issue will open the Block Ingres Trace feature based on this log`。

    ![命中日志](./www/static/img/wiki/rule_manage.png)

    ![Audit log](./www/static/img/wiki/audit_log.png)

8. Rights Profile Authority configuration

    It is used for setting permissions to precisely limit the data of which pages a user can see. For details, see Miscellaneous-Rights Management.

9. Data Source Configuration

    Example strategy: The same device is restricted to log in 1000 times in a day, then every time you log in, you need to report a piece of data, the system will classify and count, and store it in categories. What is the name of the store? This is the data source to be configured here. For this strategy, you only need to configure the data source, named login_uid, the field contains uid, and the uid type is string. Then the program can count the dimensions according to the uid and automatically calculate whether the specified threshold is exceeded within a specified time window.

    Important: Because the logic necessarily depends on time information, it is a general and required field, timestamp is the default hidden field, and the type is timestamp (accurate to seconds, integer)

    ![Data Source Configuration](./www/static/img/wiki/data_source.png)

### Call sample

1. Invoking a query service

    Assuming there is a rule with id 1, you can query whether to hit the policy by the following method
```
curl 127.0.0.1:50000/query/ -X POST -d '{"rule_id": "1", "user_id": "10000"}' -H "Content-Type:application/json"
```

2. Invoking the reporting service

    Suppose there is a data source named test, and the data source contains the data: {"ip": "string", "user_id": "string", "uid": "string"}
```
curl 127.0.0.1:50000/report/ -X POST -d '{"source_name": "test", "user_id": "10000", "ip": "127.0.0.1", "uid": "abcabc112333222", "timestamp": 1559049606}' -H "Content-Type:application/json"
```

3. About service split

    In the open source sample, in order to simplify installation and deployment, a service is included for querying and reporting. In actual scenarios, it is clear that read and write should be separated.

    1.  You can directly deploy two copies in this way, with different domain names, one for querying (the reporting interface is not accessed), and one for reporting (the querying interface is not accessed). Traffic distribution is done at the nginx layer. Modify the configuration URL_2_HANDLERS in 
    2.  risk_server.py, select the service interface you need to deploy


## Extensions to built-in functions
1. Built-in function extension without threshold

    Take the built-in function of the Whether it is an abnormal user as an example to see the code is_abnormal in aswan / buildin_funcs / sample.py

2. Built-in function Boolean policy extension with threshold

    Take the built-in function of "Number of historical logins" as an example, see the user_login_count method in aswan / buildin_funcs / sample.py. Note: The threshold calculation is not included in the built-in function. For the control flow, see aswan / buildin_funcs / base.py.


## other

###  Increase user

Considering that most enterprise users log in with domain accounts, it is recommended to use the LDAP authentication module for direct integration. But considering that everyone's scenarios are different, you can also manually add users. The sample code is as follows:
```python
# coding=utf-8
from django.contrib.auth.models import User

username = 'username'
password = 'password'
email = 'email@momo.com'
first_name = 'Test'
last_name = 'Try'
# Normal user
User.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name)
# Administrator account
User.objects.create_superuser(username=username, password=password, email=email, first_name=first_name, last_name=last_name)
```

When the addition is complete, let The User log in, and then the administrator configures The Authority.

### Authority Management

The current Authority model contains the following elements that can be configured on the corresponding page.


|Element name | Element meaning | Configuration method | Note |
| :-----| ----: | :----: | :----: |
| uri | An independent uri in the risk control management background | Automatically generated during development | Here uri is a relative path, for example: / permissions / groups / |
| uriGroup | Multiple interrelated uris can be put into a uri group | /permissions/uri_groups/ | - |
| AuthorityGroup | Multiple uri groups can be assigned to a permission group| /permissions/groups/ | - |
| User | Users are independent individuals / employees | /permissions/users/ | 1. This system does not provide the function of adding users on the interface; 2. Users can be assigned to a certain permission group, or the uri group can be directly configured |
| administrator | Is the owner of the system, has all permissions by default | Manual configuration | - |

The specific diagram is as follows::

   ![UriGroup Management](./www/static/img/wiki/permission_manage.png)

   ![Authority Group Management](./www/static/img/wiki/url_group_manage.png)

   ![User Management](./www/static/img/wiki/user_manage.png)

### Configuration related

Currently the configuration of the Django part is stored in the www / settings directory, and the configuration of the non-Django part is located in the config directory.

In order to load different configurations in different environments, we use the environment variable RISK_ENV, and the system will automatically load the corresponding configuration file through the value of this environment variable at runtime.

To facilitate project startup, when this value is not set, the system loads the configuration of the develop environment by default. When executing the test (python manage.py test), the value of RISK_ENV must be test.

### Aswan System Workflow

1.  The business party calls the query interface before the user executes, and determines whether the current behavior is intercepted according to the returned control code (this part needs to be negotiated with the business party). If it is intercepted, it will turn to 2;
2.  User action failed, go to 5;
3.  Execute business-side logic, if the end user successfully turns to 4, otherwise go to 5;
4.  The strategy of data source related to the risk control system calls the report interface to report the results for subsequent calculation by the engine, and turns to 5;
5. End directly.

#### Example

Now there is a gopher fight activity. Gophers get a small gift if they succeed.

#### Rule

The business-side rules are:
1. Users have a 10% chance of success every time they hit the gopher

The rules on the risk control side are:
1. Abnormal users cannot hit gophers-> deny
2. Limit 1 time in 30 minutes on the same uid-> deny

#### Request example

Take a normal user performing multiple actions (assuming that each execution interval is 5s) as an example:
The first time: before the user hits the mole, the query interface is called. The pass is obtained due to the missed policy, but the user is unlucky (business-side rules). If the user fails to hit the mole, the second time is ended. , Call the query interface, get a pass due to the miss strategy, and the user is lucky (business-side rules), and the mole is successful, then call report to report the data for the third time: before the user hits the mole, call the query interface, and the hit frequency Control strategy, get deny, the behavior was intercepted, the user failed to hit the mole, and ended
...
At some point, this user was judged as an abnormal user due to some rules
...
The fourth time: before the user hits the mole, call the query interface, hit the bool-type strategy (abnormal user), and get deny. This behavior is intercepted, the user fails to hit the mole, and ends

### Project code test

```shell
$ pip install coverage
$ export RISK_ENV=test
$ python www/manage.py test
$ cd tests && python run_test.py
```

> You are welcome to provide valuable comments on this project in the issue

Assignment 6: Deploying to AWS
========

[Week 6 slides](https://docs.google.com/presentation/d/12MfZcGhnR6z_NJLlHFhQYuLse-HGEMhNWSv-0CZuQCI/edit?usp=sharing)

This week you'll be learning how to setup an AWS account, spin up an EC2 instance, and deploy your app to the cloud!

Setting up your AWS Account
----

### AWS Educate
First, register for [AWS Educate](https://aws.amazon.com/education/awseducate/). This will give you $100 in free AWS credits. If you are inelligible for AWS Educate, don't worry! We'll be using `t2.micro` instances which cost $0.0116 per hour. You can start and stop these instances as you please, and even if you left your instance running for 3 months straight, you'd only have to pay `90 * 24 * 0.0116 = $25.06`.

### Set up billing alerts

The next thing we'll do is set a budget for our AWS billing account. This will help us make sure we don't end up spending too much money on our AWS instances. Go to https://console.aws.amazon.com/billing/home#/budgets and set a “cost budget” with name "DEPLOYF19”, recurring monthly, expiring, and with an end date of Dec 2019. Set the budgeted amount to be $10. In the “alerts” part, you should configure an email notification to be sent if actual costs exceed 80% of the $10 budget. You will also need to specify your email address. Do not specify “SNS topic ARN”.

### Create an EC2 instance

1. Click on (upper left) Services → Compute → EC2, “Launch Instance” (middle of screen), select “AWS Marketplace” on the left and search for "Amazon Linux 2 AMI (HVM), SSD Volume Type".

2. Select `t2.micro` then click the "Review and Launch" button.

3. Review the information and then click "Launch". You will be prompted to select an existing key pair or create a new one. You will need to create a new one. Select "Create a new key pair", name it whatever you want, and then click "Download key pair". This key pair is very important, because you won't be able to access the VM without it. After that click "Launch Instances".

### Open instance ports

Deploying your app on EC2
----
### SSH into your EC2 instance
`ssh -i ~/path/to/key.pem ec2-user@ec2-12-345-67-89.us-east-2.compute.amazonaws.com`

You can find the public DNS name of your instance by clicking on (upper left) Services → Compute → EC2, then click on the "Instances" link in the left sidebar. Select your instance and look for the "Public DNS (IPv4)" address.
### Install and setup Docker

Since we're using Amazon Linux 2 AMI, we'll have to install Docker and Git ourselves. In real life, we'd probably use either ECS to straight up deploy containers or use EC2 with a custom AMI that has Docker and Git preinstalled. We'll use Amazon Linux 2 for simplicity.

1. Update your installed packages and package cache.

    `sudo yum update -y`
    
2. Install Docker

    - `sudo amazon-linux-extras install docker`
    - Type in `Y` when prompted.

3. Start the Docker service
    
    `sudo service docker start`
    
4. Add the ec2-user to the docker group so you can execute Docker commands without using sudo.

    `sudo usermod -aG docker ec2-user`

5. Log out and log back into your EC2 instance so that docker group changes can be applied

    - `exit`
    - `ssh -i /path/to/key.pem user@example-instance.amazonaws.com`

6. Verify that the ec2-user can run Docker commands without sudo.

    `docker info`

### Open up your instance ports if needed

1. Click on (upper left) Services → Compute → EC2, then click on the "Security Groups" link in the left sidebar.
2. Select the appropriate security group for your instance (it may be automatically selected).
3. Click on the "Inbound" tab and hit "Edit".
4. Change Type to HTTP, Port Range to the port that your `models` container is bound to (as specified in `docker-compose.yml`; 8000 for example), and Source to "Anywhere". In description, write "Allow inbound web traffic."
5. Hit Save.

### Run your docker containers

1. Install git.

    `sudo yum install git`

2. Clone your repository.

    `git clone https://github.com/username/my-deploy-project.git`

3. Download `docker-compose`.

    `sudo curl -L "https://github.com/docker/compose/releases/download/1.24.1/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose`

4. Apply executable permissions to the `docker-compose` binary.

    `sudo chmod +x /usr/local/bin/docker-compose`

5. Add your instance's public DNS address to the `ALLOWED_HOSTS` list in your app's `settings.py`.

    e.g. `ALLOWED_HOSTS = ['ec2-12-345-67-89.us-east-2.compute.amazonaws.com']`
    
    You can set `ALLOWED_HOSTS = ['*']` to allow all hosts.

5. `cd` into your project directory and run `docker-compose up`.

6. Navigate to your app at `http://example-instance.amazonaws.com:8000` and verify that it is working.

7. Celebrate!

What to turn in
---------------

Please Slack us a link to your application running live on AWS!

Finally, we strongly encourage you to take time to demo in the office hours or in lab. We want to make sure not only you are writing code that works but also code that is of best practices.

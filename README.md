# aws-ecs-airflow-demo

## Setup Codepipeline
https://docs.aws.amazon.com/codepipeline/latest/userguide/connections-github.html

## Strategy
We'll set up an AWS environment to deploy every new commit of a github repository as a new EFS system versioned repo where ECR can take instructions on how builds Airflow containers and these can run on ECS, also taking instruction from said EFS versioned repo. Let's start by setting up AWS Codepipeline. 

Deploy all versions of a github repo as zip files in an s3 bucket, then call a lambda to get the newest version of the zipped file within it into an EFS configured within the Lamda function.

## Steps
- Criar repo
- Conectar AWS ao GitHub através do app na conta
- Criar S3 bucket para armazenar versões do repo
- Criar EFS e EFS Point (algumas configurações importantes)
- Criar Role Especial com Inline Policy acrescentada para Lambda poder ler do S3, ser invocada por um bucket de lá e escrever no EFS
- Criar Security groups de acesso entre Lambda, ECS e EFS
- Criar Codepipeline
- Criar VPC Endpoint para que a Lambda tenha acesso ao S3 (caso ela e o EFS estiverem em uma mesma VPC, ao contrário do S3, que nunca está)
- Criar Lambda para salvar versões do repo no S3 e EFS 

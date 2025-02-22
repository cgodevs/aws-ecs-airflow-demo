# aws-ecs-airflow-demo

## Setup Codepipeline
https://docs.aws.amazon.com/codepipeline/latest/userguide/connections-github.html

## Strategy
We'll set up an AWS environment to deploy every new commit of a github repository as a new EFS system versioned repo where ECR can take instructions on how builds Airflow containers and these can run on ECS, also taking instruction from said EFS versioned repo. Let's start by setting up AWS Codepipeline. 

Deploy all versions of a github repo as zip files in an s3 bucket, then call a lambda to get the newest version of the zipped file within it into an EFS configured within the Lamda function.

## Steps
- Criar repo (OK)
- Conectar AWS ao GitHub através do app na conta (OK)
- Criar S3 bucket para armazenar versões do repo (OK)
- Criar EFS (OK)
- Criar Role Especial com Inline Policy acrescentada para Lambda poder ler o EFS e EC2 (OK)
- Criar Lambda para salvar versões do repo no S3 e EFS
- (Opcional) Criar projeto CodeBuild, incluindo build commands, pois é interessante para desconsiderar alguns arquivos, mas não é estritamente necessário
- Criar Role para Codepipeline acessar S3 e Lambda 
- Criar Codepipeline
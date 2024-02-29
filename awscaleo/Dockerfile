FROM public.ecr.aws/lambda/python:3.12

# Copiar o arquivo da função e as dependências
COPY lambda_function.py ./
COPY requirements.txt ./

# Instalar as dependências do Python
RUN python3.12 -m pip install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

# Definir a função handler
CMD ["lambda_function.lambda_handler"]
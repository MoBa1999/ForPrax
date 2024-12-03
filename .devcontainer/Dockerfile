# syntax=docker/dockerfile:1

FROM pytorch/pytorch:2.1.0-cuda11.8-cudnn8-runtime
RUN apt-get update && apt-get install -y git screen

WORKDIR /app
SHELL ["/bin/bash", "--login", "-c"]
    
# Create the environment
COPY env.yml . 
RUN conda env create -f env.yml
CMD ["/bin/bash"]

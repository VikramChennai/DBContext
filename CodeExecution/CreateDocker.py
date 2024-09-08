import docker
import os

def load_docker():
    client = docker.from_env()

    # Get the current script's directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    dockerfile_path = os.path.join(script_dir, 'Dockerfile')

    # Build the Docker image from the script's directory
    image, _ = client.images.build(path=script_dir, dockerfile=dockerfile_path, rm=True)

    # Run the container from the built image
    container = client.containers.run(image, detach=True, tty=True)

    return container

# Remove the argument as it's not used in the function

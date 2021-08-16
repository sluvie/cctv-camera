import docker

client = docker.from_env()

container = client.containers.get("camera-01")
container_state = container.attrs['State']
print(container_state['Status'])

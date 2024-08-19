import subprocess
import yaml
from kubernetes import client, config

# Load Kubernetes configuration
config.load_kube_config()

# Define fault injection YAML
fault_injection_yaml = """
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: ratings-fault-injection
spec:
  hosts:
  -ratings
  http:
  - route:
    - destination:
        host: ratings
    fault:
      delay:
        percentage:
          value: {percentage}
        fixedDelay: {delay}s
"""

def inject_fault(ratings , percentage, delay):
    # Prepare the YAML configuration
    yaml_content = fault_injection_yaml.format(ratings = ratings , percentage=percentage, delay=delay)
    with open(f"{ratings }-fault-injection.yaml", 'w') as file:
        file.write(yaml_content)

    # Apply the fault injection using kubectl
    subprocess.run(["kubectl", "apply", "-f", f"{ratings }-fault-injection.yaml"])

def remove_fault(ratings ):
    # Remove the fault injection configuration
    subprocess.run(["kubectl", "delete", "virtualservice", f"{ratings}-fault-injection"])

if __name__ == "__main__":
    # Example usage
    inject_fault(ratings ="example-service", percentage=100, delay=5)
    # To remove the fault
    # remove_fault(ratings ="example-service")

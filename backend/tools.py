import os
""""""""
def is_docker():
    """ Sprawdza, czy aplikacja działa w kontenerze Docker. """
    try:
        if os.path.exists('/.dockerenv'):
            return True
        
        with open('/proc/1/cgroup', 'r') as f:
            if 'docker' in f.read():
                return True
        return False
    except Exception as e:
        return False
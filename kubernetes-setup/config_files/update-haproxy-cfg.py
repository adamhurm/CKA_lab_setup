import argparse, re

def build_config(args):
    default_frontend_cfg = """
frontend proxynode
    bind *:80
    bind *:6443
    stats uri /proxystats
    default_backend k8sServers
"""
    default_backend_cfg = """
backend k8sServers
    balance roundrobin
"""
    default_listen_cfg = """
listen stats
    bind :9999
    mode http
    stats enable
    stats hide-version
    stats uri /stats
"""
    with open('/etc/haproxy/haproxy.cfg', 'r+') as f:
        cfg = f.read()

        global_cfg = re.search(r'global(\n(\t|\ )+.*\n*)+\n', cfg).group(0)

        defaults_cfg = re.search(r'defaults(\n(\t|\ )+.*)+\n', cfg).group(0)
        defaults_cfg = re.sub(r'mode\shttp', 'mode\ttcp', defaults_cfg)
        defaults_cfg = re.sub(r'option\shttplog', 'option\ttcplog', defaults_cfg)

        frontend_cfg = re.search(r'frontend proxynode(\n(\t|\ )+.*)+\n', cfg)
        if frontend_cfg:
            frontend_cfg = frontend_cfg.group(0)
        else:
            frontend_cfg = default_frontend_cfg

        backend_cfg = re.search(r'backend k8sServers(\n(\t|\ )+.*)+\n', cfg)
        if backend_cfg:
            backend_cfg = backend_cfg.group(0)
        else:
            backend_cfg = default_backend_cfg

        listen_cfg = re.search(r'listen stats(\n(\t|\ )+.*)+\n', cfg)
        if listen_cfg:
            listen_cfg = listen_cfg.group(0)
        else:
            listen_cfg = default_listen_cfg

        add_node = lambda c, n, i: c+f'    server {n}  {i}:6443 check\n'
        for node_pair in args.nodes:
            name, ip = node_pair.split('=')
            backend_cfg = add_node(backend_cfg, name, ip)

        f.seek(0)
        f.write(global_cfg+'\n'+defaults_cfg+'\n'+frontend_cfg+'\n'+backend_cfg+'\n'+listen_cfg+'\n')
        f.truncate()

def main():
    parser = argparse.ArgumentParser(prog='UpdateHaproxyCfg',
                                    description='Update haproxy.cfg for HA k8s cluster')
    parser.add_argument('nodes', nargs='+', help='provide list: node1=ip1 name2=ip2 ...',
                        metavar="KEY=VALUE")
    args = parser.parse_args()
    build_config(args)

if __name__ == '__main__':
    main()

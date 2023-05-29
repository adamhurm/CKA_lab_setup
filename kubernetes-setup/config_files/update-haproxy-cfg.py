import argparse, re

def build_config(args):
    listen_cfg = """
listen stats
    bind :9999
    mode http
    stats enable
    stats hide-version
    stats uri /stats
    """
    frontend_cfg = """
frontend proxynode
    bind *:80
    bind *:6443
    stats uri /proxystats
"""
    backend_cfg = """
backend k8sServers
    balance roundrobin
"""

    with open('haproxy.cfg') as f:
        cfg = f.read()
        read_defaults_cfg = re.search(r'defaults(\n(\t|\ )+.*)+\n', cfg).group(0)
        defaults_cfg = re.sub(r'mode\shttp', 'mode\ttcp', read_defaults_cfg)
        defaults_cfg = re.sub(r'option\shttplog', 'option\ttcplog', defaults_cfg)
        cfg.replace(read_defaults_cfg, defaults_cfg)

        add_node = lambda c, n, i: c+f'    server {n}  {i}:6443 check\n'
        for node_pair in args.nodes:
            name, ip = node_pair.split('=')
            backend_cfg = add_node(backend_cfg, name, ip)
        print(cfg + frontend_cfg + backend_cfg + listen_cfg)

def main():
    parser = argparse.ArgumentParser(prog='UpdateHaproxyCfg',
                                    description='Update haproxy.cfg for HA k8s cluster')
    parser.add_argument('nodes', nargs='+', help='provide list: node1=ip1 name2=ip2 ...',
                        metavar="KEY=VALUE")
    args = parser.parse_args()
    build_config(args)

if __name__ == '__main__':
    main()

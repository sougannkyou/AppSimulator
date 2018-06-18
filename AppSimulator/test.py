# coding=utf-8
import xmlrpc.client
from dbDriver import MongoDriver, RedisDriver

MDB = MongoDriver()
RDB = RedisDriver()

def test():
    tasks = MDB.get_tasks(status='wait')
    for task in tasks:
        rpcServers = MDB.get_rpc_server(appName=task['appName'])
        print(rpcServers)
        for server in rpcServers:
            rpcServer = "http://" + server['ip'] + ":" + str(server['port'])
            with xmlrpc.client.ServerProxy(rpcServer) as proxy:
                # ret = proxy.runTasks(app_name, tasks_cnt)
                free_mem = proxy.get_free_mem()
                print(free_mem)
                if float(free_mem) > 1:
                    proxy.get_free_mem()


test()
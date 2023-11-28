#!/usr/bin/env python

from getpass import getpass

from radkit_common.utils.ssl import create_public_ssl_context
from radkit_service.control_api import ControlAPI
from radkit_service.webserver.models.users import NewRemoteUser

from stopwatch import StopWatch

verify = create_public_ssl_context(verify=False, use_obsolete_ciphers=False)

with ControlAPI.create(base_url="https://localhost:8081/api/v1", admin_name="superadmin", admin_password=getpass("Password: "), http_client_kwargs=dict(verify=verify)) as service:
    stopwatch = StopWatch()

    users = []
    for i in range(10):
        user = NewRemoteUser(
            username=f"user.{i}@cisco.com",
            fullname=f"Full Name {i}",
            description="Some description"
        )
        users.append(user)

    print(f"creating {len(users)} users")
    stopwatch.start()
    result = service.create_remote_users(users)
    stopwatch.stop()
    stopwatch.print_delta(f"users created in ")
    # print(type(result))
    #print(result.results)

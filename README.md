# multi_ten

## run: pip install -r requirements.txt


# Setting up environment for the subdomains on windows
Because you are running on local hosts, you will need to add each subdomain you
want to create in the windows hosts file.

The windwos hosts file can be found at C:\windows\System32\drivers\etc\hosts

For example to add a new subdomain: xyz, you will need to add the following line to your host file:

127.0.0.1 xyz.wisemen

This will make it possible to access the address: xyz.wisemen:8000 once the user regisers.

This is only necessary at development. At production, you will need to configure subdomain by using
the wildcard: *.wisemen.com so that it covers all possible subdomains without having to manually enter each 
subdomain.


# Setting up database for the first time
1. Install Postgres
2. Create new database `wisemen`
3. Delete default public schema and create default schema `www`
4. Run command to perform initial migration of schema to `www`

   python tenant_context_manage.py www migrate

5. Save and exit.


# Run program
1. Start server
2. load wibsite by entering www.wisemen:8000/account/register
3. Register a new user
4. System creates a new schema, performs migrations for new schema, changes current schema from `www`
to new schema, and logs in new user.


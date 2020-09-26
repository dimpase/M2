The interactive shell is the web interface running on [Habanero](http://habanero.math.cornell.edu:3690/)

The codebase can be found at the repository https://github.com/fhinkel/InteractiveShell
The repository includes files needed for the frontend, backend, as well as Dockerfiles and Vagrantfiles used to create containers and virtual machines.

The webserver can be run on a basic virtual machine by using Vagrant
```
git clone git@github.com:fhinkel/InteractiveShell.git
cd InteractiveShell/setup/basic
vagrant up
```
Other templates for virtual machines can be found in the `setup` directory. For example the vagrantfile in the `twoMachines` creates two virtual machines, one for the webserver and one for the Macaulay2 Docker containers. 

Alternatively, the server can also be run locally
```
git clone git@github.com:fhinkel/InteractiveShell.git
cd InteractiveShell
npm install
npm start
```


By default, the interface should be accessible on any web browser at `localhost:8002`.
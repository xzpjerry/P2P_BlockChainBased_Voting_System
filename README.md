# P2P_BlockChainBased_Voting_System
## Demo
- Client demo is at http://35.197.84.58:8080/
- Miner demos address are in the Client demo's "register miner nodes" page.

## Docker image usage:
### Build from scratch:

- docker build -t [Anyname You Want] [Location of the Dockerfile]
- Run its bash

### Use my prebuild image:
```
docker run -it -v <Folder to be mounted>:/host -p 8080:8080 xzpjerry/prjtestt bash
```

## After pulling the image
```
cd /project
make veryclean
make node_start
make client_start
```
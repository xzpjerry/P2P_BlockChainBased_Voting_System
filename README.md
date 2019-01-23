# P2P_BlockChainBased_Voting_System

## Docker image usage:
### Build from scratch:
- docker build -t <Anyname You Want> <Location of the Dockerfile>

### Use my prebuild image:
```
docker run -it -v <Folder to be mounted>:/host -p 8080:8080 xzpjerry/prjtestt bash
```
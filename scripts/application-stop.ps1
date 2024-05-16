c:\temp\codedeploy-agent.msi /quiet /l c:\temp\host-agent-install-log.txt
powershell.exe -Command Restart-Service -Name codedeployagent
docker rm -f crawl_container
choco install docker-cli
c:\temp\codedeploy-agent.msi /quiet /l c:\temp\host-agent-install-log.txt
#powershell.exe -Command Restart-Service -Name codedeployagent
#$containerName="crawl_container"
#$containerExists = docker ps -a --format '{{.Names}}' | Where-Object { $_ -eq $containerName }
#if ($containerExists) {
#    # 컨테이너가 존재하면, 컨테이너를 종료합니다.
#    docker stop $containerName
#    Write-Host "컨테이너 $containerName 이 종료되었습니다."
#} else {
#    # 컨테이너가 존재하지 않으면, 메시지를 출력합니다.
#    Write-Host "컨테이너 $containerName 이 존재하지 않습니다."
#}
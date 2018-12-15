echo "Install Python requirements.txt"
pip3 install -r deploy/requirements.txt
echo "Install docker"
docker-compose -f dev.yml up -d
echo "Waiting 5 seconds to next step..."
sleep 5
echo "Init secret.key..."
echo $RANDOM | md5sum | head -c 10 > $PWD/data/config/secret.key

echo "Init postgres database...."
n=0
while [ $n -lt 5 ]
do
    python manage.py migrate --no-input &&
    python manage.py inituser --username=root --password=rootroot --action=create_super_admin &&
    echo "from options.options import SysOptions; SysOptions.judge_server_token='$JUDGE_SERVER_TOKEN'" | python manage.py shell &&
    echo "from conf.models import JudgeServer; JudgeServer.objects.update(task_number=0)" | python manage.py shell &&
    break
    n=$(($n+1))
    echo "Failed to migrate, going to retry..."
    sleep 8
done

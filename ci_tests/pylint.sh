#!/bin/bash

# Pylint report
# Miguel Colom, 2016

modulesDir="ipolDevel/ipol_demo/modules/"
modules="core archive blobs demoinfo demorunner proxy"
report="pylint_report.txt"

#truncate -s 0 ${report}
today=$(date)
echo "IPOL PyLint report on ${date}" > ${report}
echo >> ${report}

# PyLint test on each IPOL module
for module in ${modules}
do
    echo "**** MODULE: ${module}" >> ${report}
    sudo -u ipol pylint ~/${modulesDir}${module}/*.py >> ${report}
done

# Send report by email
sendTo=$(cat /home/ipol/ipolDevel/ci_tests/send_to.txt)
echo "PyLint report" | sudo -u ipol mutt -a ${report} -s "[ipolDevel] CI test: PyLint" -- ${sendTo}

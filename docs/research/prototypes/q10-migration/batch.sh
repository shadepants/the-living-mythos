for s in 1 2 3; do for v in base free overlap share; do echo "$v map $s 0.9"; done; for v in free share; do echo "$v map $s 1.5"; done; done | xargs -P 2 -L 1 python3 q10.py > batch1.txt 2>&1
for s in 1 2 3 4 5; do for v in base share overlap; do for m in 0.9 1.5; do echo "$v island $s $m"; done; done; done | xargs -P 2 -L 1 python3 q10.py > island1.txt 2>&1
echo DONE >> batch1.txt

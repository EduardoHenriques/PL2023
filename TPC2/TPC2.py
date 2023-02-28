import sys
import re

if __name__ == '__main__':
        switch = True
        total = 0
        #procura on/ON
        look_On = re.compile(r'(?i)On')
        #procura off/OFF
        look_Off = re.compile(r'(?i)Off')
        
        for line in sys.stdin:
            line = line.strip()
            if re.search(look_On, line):
                switch = True
                print("Sum on")
            elif re.search(look_Off, line):
                switch = False
                print("Sum off")

            if switch:
                nums = re.findall("\d+", line)
                for n in nums:
                    total += int(n)

            if "=" in line:
                print(f"Resultado: {total}")
                total = 0




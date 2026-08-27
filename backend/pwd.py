from argon2 import PasswordHasher
ph = PasswordHasher(time_cost = 3, memory_cost = 65536, parallelism = 4)
#pwd = ph.hash('officer001')
#pwd = ph.hash('officer002')
#pwd = ph.hash('fieldinsp001')
pwd = ph.hash('fieldinsp002')
pwd = ph.hash('fieldinsp003')

print(pwd)

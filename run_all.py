import os
import sys
import subprocess
import time
import shutil

PYTHON = sys.executable


def print_ascii(msg: str):
	# Avoid Unicode emojis on Windows consoles with cp1252
	sys.stdout.write(msg + "\n")
	sys.stdout.flush()


def check_and_install_requirements():
	print_ascii("[SETUP] Ensuring dependencies are installed...")
	req = os.path.join(os.path.dirname(__file__), 'requirements.txt')
	if not os.path.isfile(req):
		print_ascii("[WARN] requirements.txt not found; skipping install")
		return True
	try:
		subprocess.run([PYTHON, '-m', 'pip', 'install', '--user', '-r', req], check=True)
		return True
	except subprocess.CalledProcessError as e:
		print_ascii(f"[ERROR] Failed to install requirements: {e}")
		return False


def setup_database():
	print_ascii("[DB] Running database setup...")
	try:
		res = subprocess.run([PYTHON, 'setup_database.py'], check=True)
		return res.returncode == 0
	except subprocess.CalledProcessError as e:
		print_ascii(f"[ERROR] Database setup failed: {e}")
		return False


def start_backend(env=None):
	print_ascii("[BACKEND] Starting API at http://localhost:8000 ...")
	# Use -u for unbuffered output; pass env to override DB creds if needed
	return subprocess.Popen([PYTHON, '-u', 'enhanced_api.py'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=env)


def start_frontend():
	print_ascii("[FRONTEND] Serving static files at http://localhost:5000 ...")
	return subprocess.Popen([PYTHON, '-u', 'serve_frontend.py'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)


def stream_output(name, proc):
	try:
		if proc.stdout is None:
			return
		for line in iter(proc.stdout.readline, b''):
			if not line:
				break
			try:
				decoded = line.decode('utf-8', errors='ignore').rstrip()
			except Exception:
				decoded = str(line).rstrip()
			print_ascii(f"[{name}] {decoded}")
	finally:
		try:
			proc.stdout.close()
		except Exception:
			pass


def main():
	os.chdir(os.path.dirname(__file__))
	ok = check_and_install_requirements()
	if not ok:
		print_ascii("[EXIT] Unable to continue without dependencies.")
		sys.exit(1)

	if not setup_database():
		print_ascii("[EXIT] Database setup failed. Check your MySQL service and credentials.")
		sys.exit(1)

	# Inherit environment; user may set DB_HOST/DB_USER/DB_PASSWORD/DB_NAME
	env = os.environ.copy()

	backend = start_backend(env)
	time.sleep(1.0)
	frontend = start_frontend()

	print_ascii("[INFO] Project is starting up. Open these URLs:")
	print_ascii("       - API:    http://localhost:8000/api/health")
	print_ascii("       - Frontend: http://localhost:5000/")
	print_ascii("[INFO] Press Ctrl+C to stop.")

	try:
		# Stream outputs interleaved
		while True:
			alive = False
			for name, proc in (('API', backend), ('WEB', frontend)):
				if proc.poll() is None:
					alive = True
					if proc.stdout and proc.stdout.peek():
						stream_output(name, proc)
			if not alive:
				break
			time.sleep(0.2)
	except KeyboardInterrupt:
		print_ascii("\n[INFO] Shutting down...")
	finally:
		for proc in (backend, frontend):
			try:
				proc.terminate()
			except Exception:
				pass
		for proc in (backend, frontend):
			try:
				proc.wait(timeout=5)
			except Exception:
				pass
		print_ascii("[DONE] Stopped.")


if __name__ == '__main__':
	main()

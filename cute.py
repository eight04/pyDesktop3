#! python3

from xcute import cute, run_task

def readme():
	"""Live reload readme"""
	from livereload import Server, shell
	server = Server()
	server.watch("README.rst", lambda: run_task("readme_build"))
	server.serve(open_url_delay=1, root="build/readme")
	
cute(
	pkg_name = "desktop",
	test = ["pyflakes {pkg_name} setup.py", 'readme_build'],
	bump_pre = 'test',
	bump_post = ['clean', 'dist', 'release', 'publish', 'install'],
    clean = 'x-clean build dist',
	dist = 'python setup.py sdist bdist_wheel',
	release = [
		'git add .',
		'git commit -m "Release v{version}"',
		'git tag -a v{version} -m "Release v{version}"'
	],
	publish = [
		'twine upload dist/*',
		'git push --follow-tags'
	],
	install = 'pip install -e .',
	readme_build = [
		'python setup.py --long-description | x-pipe build/readme/index.rst',
		'rst2html5.py --no-raw --exit-status=1 --verbose '
			'build/readme/index.rst build/readme/index.html'
	],
	readme_pre = "readme_build",
	readme = readme
)

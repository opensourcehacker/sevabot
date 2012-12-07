# vi: set ft=ruby :

Exec { path => [ "/bin/", "/sbin/" , "/usr/bin/", "/usr/sbin/" ] }
Package { ensure => "installed" }



define wget($source, $destination) {
	if $http_proxy {
		exec { "wget-$name":
			command => "/usr/bin/wget --output-document=$destination $source",
			creates => "$destination",
			environment => [ "HTTP_PROXY=$http_proxy", "http_proxy=$http_proxy" ],
		}
	} else {
		exec { "wget-$name":
			command => "/usr/bin/wget --output-document=$destination $source",
			creates => "$destination",
		}
	}
}


define git_clone($source, $destination, $owner) {
  exec { "git_clone-$name":
    command => "git clone $source $destination",
    creates => "$destination",
  }
  
  file { "$destination":
    ensure => directory,
	recurse => true,
	owner => "$owner",
    group => "$owner",
  }
  
}



node default {
  exec {'apt_update':
    command => 'apt-get update --quiet && apt-get upgrade --quiet --assume-yes'
  }

  
  $packages = [ 
   "xvfb", 
   "fluxbox", 
   "x11vnc",
   "dbus",
   
   "python-gobject-2",
   "curl",
   "git",
   
   "libasound2",
   "libqt4-dbus",
   "libqt4-network",
   "libqtcore4",
   "libqtgui4",
   "libxss1",
   "libpython2.7",
   "libqt4-xml",
   "libaudio2",
   "libmng1",
   "fontconfig",
   "liblcms1",
   
   "lib32stdc++6",
   "lib32asound2",
   "ia32-libs",
   "libc6-i386",
   "lib32gcc1",
  ]

  package { $packages:
    require => Exec['apt_update'],
  }
  
  user { "skype":
    ensure => 'present',
    managehome => true,
    shell => "/bin/bash",
    password => "'$'6'$'/kio47YP'$'St/on312sQm.AV4RVDYQVmrJ9gUkKUKcuYts.LMXbxVet.TSRsBuhkv9w1E8VuWu4Ze6RxASby9.CwlPQY7lQ.",
    require => Package[$packages],
  }
  
  wget{"skype-deb": 
    source => "http://www.skype.com/go/getskype-linux-beta-ubuntu-64", 
    destination => "/home/skype/skype-linux-beta.deb",
    require => User['skype'],
  }
  
  package { "skype-package":
    provider => dpkg,
    ensure   => 'present',
    source   => "/home/skype/skype-linux-beta.deb",
    require => [ Wget[skype-deb], Package[$packages] ],
  }
  
  git_clone{"sevabot":
    source => "https://github.com/opensourcehacker/sevabot.git",
    destination => "/home/skype/sevabot",
    owner => "skype",
    require => User['skype'],
  }
  
  exec { "virtualenv":
    command => "curl -L -o /home/skype/sevabot/virtualenv.py https://raw.github.com/pypa/virtualenv/master/virtualenv.py",
    creates => "/home/skype/sevabot/virtualenv.py",
    require => Git_clone["sevabot"],
  }
  
}

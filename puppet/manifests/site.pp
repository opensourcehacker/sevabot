# vi: set ft=ruby :

Exec { path => [ "/bin/", "/sbin/" , "/usr/bin/", "/usr/sbin/" ] }

class apt {
 Package {
    require => Exec['apt-get_update']
  }

  exec {'apt-get_update':
    command     => 'apt-get update',
    refreshonly => true,
  }
}

class skype-bot-packages {
  Package { ensure => "installed" }
  $enhancers = [ 
    "xvfb", 
    "fluxbox", 
    "x11vnc",
    "dbus",
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
    "liblcms1"
  ]

  package { $enhancers: }
}

node default {
  include apt
  include skype-bot-packages
}

notice("Hello world!")

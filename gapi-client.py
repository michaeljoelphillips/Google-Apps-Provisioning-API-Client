#!/usr/bin/python
#
# gapi-client.py - Google Provisioning API Client
# Copyright (C) 2011 Michael Phillips <michaeljoelphillips@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
# Distributed under the GNU General Public License, version 2.0.

"""A Command Line client for Google Apps user configuration used with Google Provisioning API.

	ProvisioningClient: Connects to Google API for Apps user configuration.
"""

__author__ = "Michael Phillips <michaeljoelphillips@gmail.com>"


import gdata.apps.service
from optparse import OptionParser
import getpass
import sys

parser = None
options = None

class ProvisioningClient(object):
	"""ProvisioningClient from the User Provisioning Client API."""

	def __init__(self, email, domain, password):
		"""Constructor for ProvisioningClient object.

		Takes admin information and authenticates with the Google API Servers for
		later user modification.

		Args:
			email: [string] The email address for the administrator account.
			domain: [string] The domain the administrator belongs to.
			password: [string] The password for the administrator account.
		"""

		self.client = gdata.apps.service.AppsService(email=email, domain=domain, password=password)
		self.client.ProgrammaticLogin()


	def executeCommand(self, method, user_name, password=None, first_name=None, last_name=None):
		"""Function that handles the various methods for user configuration.

		Takes all parameters passed and specifies how to handle them based on
		the user assigned valude of the method variable.

		Args:
			method: [string] The method assigned to be performed on the user.
			user_name: [string] The user name of the user for action to be taken on.
			password: [optional] The password for the user for action to be taken on.
			first_name: [optional] The first name of the new user to be created.
			last_name: [optional] The last name of the new user to be created.
		"""

		if method == 'create':
			print "Creating ", user_name
			if (first_name is None):
				first_name = raw_input("First Name: ")
			if (last_name is None):
				last_name = raw_input("Last Name: ")
			if (password is None):
				password = getpass.getpass(prompt = "New Password: ")
				verify_password = getpass.getpass(prompt = "Verify Password: ")
				if (verify_password != password):
					print "Passwords do not match!"
					sys.exit()
			print self.client.CreateUser(user_name=user_name, given_name=first_name, family_name=last_name, password=password)
		elif method == 'retrieve':
			print self.client.RetrieveUser(user_name=user_name)
		elif method == 'delete':
			print self.client.DeleteUser(user_name=user_name)
		elif method == 'retrieve_all':
			print self.client.RetrieveAllUsers()
		elif method == 'update':
			user = self.client.RetrieveUser(user_name=user_name)
			user.login.password = password
			self.client.UpdateUser(user_name, user)
		else:
			print "No method available..."


def main():
	"""Uses Google Provisioning API to allow command line user configuration."""

	usage = "Usage: %prog [options]"
	global parser
	global options

	parser = OptionParser(usage=usage)
	parser.add_option("--adminlogin", help="The Administrator Email address for the domain.")
	parser.add_option("--adminpassword", help="The Administrator Password for the domain.")
	parser.add_option("-d", "--domain", help="The Domain to configure.")
	parser.add_option("-m", "--method", choices=["create", "retrieve", "retrieve_all", "delete", "update"], help="The method to be used.  Select from create, delete, update, retrieve, retrieve_all.")
	parser.add_option("-u", "--username", help="The user in which to perform actions.")
	parser.add_option("-p", "--password", help="The password to be updated for the user.")
	parser.add_option("-f", "--firstname", help="Optional.  Firstname of new user.")
	parser.add_option("-l", "--lastname", help="Optional.  Lastname of new user.")
	(options, args) = parser.parse_args()

	if (options.method is None or options.method != "retrieve_all" and options.username is None or options.method == "update" and options.password is None):
		parser.print_help()
		return

	if (options.adminlogin is None):
		options.adminlogin = raw_input("Administrator Email: ")
	if (options.domain is None):
		options.domain = raw_input("Domain: ")
	if (options.adminpassword is None):
		options.adminpassword = getpass.getpass(prompt = "Please Authenticate: ")
	objectvar = ProvisioningClient(options.adminlogin, options.domain, options.adminpassword)
	objectvar.executeCommand(options.method, options.username, options.password, options.firstname, options.lastname)

if __name__ == "__main__":
	main()


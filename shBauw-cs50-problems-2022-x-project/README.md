# Python Password Manager + Generator
#### Video Demo: <https://youtu.be/VkbIIdJwsTs>
#### Description:
##### Purpose: 
A python password manager with rudimentary validation of master password, a built in password generator and basic encryption security for account details.
I decided to make this after hearing David speak about the importance of using a password manager, deciding to see under the hood of these programs.
##### Design Choices:
Initially, I planned to make a website with credentials being stored inside of an sql table but ultimately rejected that idea, going for the more secure, completely offline alternative of an application on the computer itself, getting the idea itself from the increased security of offline cryptocoin wallets in comparison to cloud-stored wallets, as it can even be put on a USB and taken with you everywhere.
Creating this, I wanted to make an accompanying chrome extension that could show the correct credentials after reading the domain of the currently focused tab. This did not end up working as you can not interact with local files through a chrome extension. This is for security purposes but stunted this idea.
I also decided to create a simple GUI due to the fact that this would greatly reduce the amount of possible errors that could occur in comparison to the commandline and would also streamline the application, making it more interactive for an average user as well.
Additionally, I went with a very simple GUI as I wished to focus on the code itself, even moving away from strict commandline was only due to the pros heavily outweighing the losses.
Furthermore, the code is a little bit clunky as you have to choose whether to add or view as this would allow for the table to be refreshed in a much simpler way.
##### The Files:
passwordManager.py is the application itself, containing code to add to passwords.txt, generate passwords to specification and view stored passwords
gen.key stores the key generated when the program was first run. This code has been commented out but can be utilised again for a completely fresh start by deleting gen.key, uncommenting the code and running the program again, remembering to comment it again before the next use otherwise decryption will not work.
passwords.txt stores delimited strings containing full credentials that have been encrypted, storing one per line.
passwords.csv is an intermediary file utilised in computation, after decrypting the strings in passwords.txt, they are stored in the csv file for easier display.
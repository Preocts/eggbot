# Chat Kudos Module v1.0.0

### Kudos points brought to Discord

Chat Kudos are points that can be granted, or taken, from server members by simply mentioning their name and having "+"s or "-"s following the mention.  The bot will reply with a customizable message, tell you how many kudos were just received, and keep a running tally.

There is a leader-board built in that, by default, displays the top ten Kudos holders in the guild. Fun for the competitive natured souls.

Control who can use Kudos with the allow lists. Out-of-the-box Kudos only allows roles and users on these lists to use the module. The server owner is always on the allow list. This lets you quickly grant access to your choice of members if you want to keep the reigns tight.

Don't care who uses Kudos? Want to see just how quickly your chat devolves into a free-for-all point battle? Simply unlock the module and everyone can add/remove Kudos, show the leader-board, and request help docs be sent to their DM.

Chat line configuration controls are always restricted to allowed users only.

---

## Granting and Removing Kudos:

```
Me> @Some_Member +++
Egg_Bot> 3 points to Some_Member

Me> @Some_Member ---
Egg_Bot> 3 points from Some_Member

me> @Some_Member +Awesome-Sauce+
Egg_Bot> 1 points to Some_Member
```

The mention can be located anywhere in the chat mention. The "+" and "-" need to follow the mention immediately and not have spaces separating them.

---

#### Basic Commands:

*Open to anyone allowed to run Kudos*

**kudo!board** (#)

- Show top scoreboard in the channel the command is run. Scoreboard defaults to the top 10 Kudos holders but you can provide a number to specify how many results you want to display.

**kudo!help**

- A short version of this document will be DM'ed in Discord

---

#### Configuration Commands:

- *Can only be run by members on the user allow list (locked or unlocked)*
- *Server owner and bot owner always has access to these*
- *Commands are typed into any channel the bot is in*

### `kudos!max [#]`

- Set the maximum number of points a single ChatKudos chat provides or removes
- Set this to 0 or -1 to allow unlimited points

### 'kudos!gain [message to display on gain]'

### `kudos!loss [message to display on loss]'

- Define a custom message for when a member gains or loses Kudos.
  - `[POINTS]` will be replaced with # of points
  - `[NAME]` will be replaced with the display name of who is gaining/losing Kudos
  - `[TOTAL]` will be replaced with the total points for that person

*examples*
```
kudos!gain Fantastic [NAME], have [POINTS] Kudos points. You now have [TOTAL] in total.

kudos!loss That one cost you [POINTS] points, [NAME]. That leaves you [TOTAL] in total.
```

**kudo!set user** [@mention] (@mention)...

**kudo!set role** [@role_name] (@role_name)...

- Controls what is on the allow lists for users and roles. This acts as a toggle. Adding a user who is already on the list will remove them. Same for roles
- You can add as many users or roles as desired in one call (2000 character limit)
- You can even mix and match roles and users, these are aliased for clarity but run the same functions.

**kudo!set lock**

- Turns lock on or off.
- When Kudos is locked only allowed users/roles can use Kudos. Server owner always has access to Kudos regardless of lock.
- This is the same as adding @everyone to role allow list without pinging the entire server.

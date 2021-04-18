# Chat Kudos Module v1.0.0

## Kudos points brought to Discord

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

Me> @Some_Member +Awesome-Sauce+
Egg_Bot> 1 points to Some_Member
```

The mention can be located anywhere in the chat mention. The "+" and "-" need to follow the mention immediately and not have spaces separating them.

---

## Basic Commands:

**Open to anyone allowed to run Kudos**

### `kudos!board (#)`

- Show high-score board in the channel
- Scoreboard defaults to the top 10 Kudos holders but you can provide a number to specify how many results you want to display

### `kudos!help`

- A link back to this page

---

## Configuration Commands:

- *Can only be run by members on the user allow list (locked or unlocked)*
- *Server owner always has access to these*
- *Commands are typed into any channel the bot is in*

### `kudos!max [#]`

- Set the maximum number of points a single ChatKudos chat provides or removes
- Set this to 0 or -1 to allow unlimited points

### `kudos!gain [message to display on gain]`

### `kudos!loss [message to display on loss]`

- Define a custom message for when a member gains or loses Kudos.
  - `[POINTS]` will be replaced with # of points
  - `[NAME]` will be replaced with the display name of who is gaining/losing Kudos
  - `[TOTAL]` will be replaced with the total points for that person

*examples*
```
kudos!gain Fantastic [NAME], have [POINTS] Kudos points. You now have [TOTAL] in total.

kudos!loss That one cost you [POINTS] points, [NAME]. That leaves you [TOTAL] in total.
```

### `kudos!user [@mention (@mention ...)]`
### `kudos!role [@role_name (@role_name ...)]`
- Add/Remove users and roles from the allow list
- When locked (see below) these users and roles will be able to use ChatKudos
- Guild owner, by default, always have access
- If a user or role is not on the list it will be added, otherwise it is removed
- You can mix and match roles and users using either command

### `kudos!lock`
- Toggles lock on or off
- When Kudos is locked only allowed users/roles can use Kudos
- Server owner always has access to Kudos regardless of lock

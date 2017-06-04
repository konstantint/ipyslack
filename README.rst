=================================================
IPython Magic for sending notifications to Slack
=================================================

Installation
------------
::

    $ pip install ipyslack
    
Usage
-----
 1. Load the extension::

    %load_ext ipyslack

 2. Configure Slack API::

    %slack_setup -t <api_token> -c <target_channel>

    To obtain the API token visit `this page <https://api.slack.com/custom-integrations/legacy-tokens>`_.
    The ``<target_channel>`` parameter may either denote a channel (e.g. ``#general``) or a user (e.g. ``@me``).
    
    Adding the option ``-u`` to ``%slack_setup`` will make yourself the sender of all messages. Otherwise (default) the messages originate from ``slackbot``.

 3. Now adding::

    %%slack_notify <message>

  at the top of any cell will send ``<message>`` to ``<target_channel>`` whenever cell execution is completed. 

  The patterns ``{out}`` and ``{err}`` within ``<message>`` will be substituted with stdout or stderr from the cell's execution. The pattern ``{exc}`` denotes the exception (if any was thrown). The string ``\n`` denotes a new line. 

  Example::

     %%slack_notify *Completed!* :heavy_plus_sign:\nStdout: {out}\nStderr: {err}\nException: {exc}

 4. In addition, the line-magic ``%slack_send <message>`` lets you send notifications about partial results. E.g.::

      %%slack_notify All done. {exc}
      ... computation ...
      %slack_send Half-way!
      ... computation ...

See also
--------

* IPyTelegram: https://github.com/kalaidin/ipytelegram/


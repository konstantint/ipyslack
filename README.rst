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
    
   Adding the option ``-u true`` to ``%slack_setup`` will make yourself the sender of all messages. Otherwise (default) the messages originate from ``slackbot``.

   In order to avoid having to write the API token in every notebook, you can create a file containing the same configuration line::
   
     -t <api_token> -c <target_channel> -u false
    
   You can then load this configuration in the notebook by invoking::
   
     %slack_setup <filename>
     
   Even simpler, if you don't call ``%slack_setup`` at all, the extension will try to auto-configure itself on first use
   by searching for the files ``~/.ipyslack.cfg`` and ``.ipyslack.cfg`` (in this order) and
   trying to load configuration from these.
   
   Later files in this search order override the settings of the previous ones. That is, you can specify ``-t <api_token> -c #default_group`` 
   in the global ``~/.ipyslack.cfg``, and only override ``-c #project_group`` in the local ``.ipyslack.cfg``.
   
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


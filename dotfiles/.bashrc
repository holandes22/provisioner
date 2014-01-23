[[ $- != *i* ]] && return

PS1='\[\033[01;32m\]\u@\[\033[01;34m\]\h\[\033[00m\]:\w$(__git_ps1 "\[\e[32m\][%s]\[\e[0m\]")$ '

# enable color support of ls and also add handy aliases
if [ -x /usr/bin/dircolors ]; then
    test -r ~/.dircolors && eval "$(dircolors -b ~/.dircolors)" || eval "$(dircolors -b)"
    alias ls='ls --color=auto'

    alias grep='grep --color=auto'
    alias fgrep='fgrep --color=auto'
    alias egrep='egrep --color=auto'
fi

# some more ls aliases
alias ll='ls -alF'
alias la='ls -A'
alias l='ls -CF'

# enable programmable completion features (you don't need to enable
# this, if it's already enabled in /etc/bash.bashrc and /etc/profile
# sources /etc/bash.bashrc).
if ! shopt -oq posix; then
  if [ -f /usr/share/bash-completion/bash_completion ]; then
    . /usr/share/bash-completion/bash_completion
  elif [ -f /etc/bash_completion ]; then
    . /etc/bash_completion
  fi
fi

#==================
# Personal settings
#==================

export EDITOR=vim
export TERM=screen-256color

DOTFILES_FOLDER=$HOME/provisioner/dotfiles
COMPLETION_FOLDER=$DOTFILES_FOLDER/completion

# Completion
# ==========
COMPLETION_SCRIPTS='fabric tmuxinator git-flow vagrant'
for COMPLETION_SCRIPT in $COMPLETION_SCRIPTS
do
    source $COMPLETION_FOLDER/$COMPLETION_SCRIPT.bash
done

if [ -e "/etc/arch-release" ]
then
    source /usr/share/git/completion/git-completion.bash
    source /usr/share/git/completion/git-prompt.sh
fi

# tmux completion
if [ -e "/etc/arch-release" ]
then
    source /usr/share/bash-completion/completions/tmux
else
    source /usr/share/doc/tmux/examples/bash_completion_tmux.sh
fi


# virtualenvwrapper
export WORKON_HOME=$HOME/virtualenvs
export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python2.7
if [ -e "/etc/arch-release" ]
then
    source /usr/bin/virtualenvwrapper.sh
else
    source /usr/local/bin/virtualenvwrapper.sh
fi

# Dev General
# ===========

export PATH=$PATH:/opt/vagrant/bin:$HOME/xpyv/bin
PATH="$(ruby -e 'puts Gem.user_dir')/bin:$PATH"

# Dev work
# =========
XIVREPOS=$HOME/xiv-repos
XPYV_BIN=$HOME/xpyv/bin
export XPYVPATH=$XIVREPOS/xsf/deps/pyne
alias runtests='xpyv $XPYV_BIN/nosetests -a !integration_test,!windows_test,!tau_test '
alias dev-xsf='export PYTHONPATH=/home/pablo/xiv-repos/xsf:/home/pablo/xiv-repos/xsf/deps/pyne;source ~/virtualenvs/xsf/bin/activate; cd ~/xiv-repos/xsf'
alias dev-hak='export PYTHONPATH=$XIVREPOS/hak/lib:$XIVREPOS/hak/deps/xiv_xsf:$XIVREPOS/hak/deps/pyne:$XIVREPOS/hak/deps/xhop;source /home/pablo/virtualenvs/hak/bin/activate; cd $XIVREPOS/hak'

### Added by the Heroku Toolbelt
export PATH="/usr/local/heroku/bin:$PATH"

# Aliases
# =======

alias ..='cd .. '

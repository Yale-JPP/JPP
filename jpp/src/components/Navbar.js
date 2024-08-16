import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import './Navbar.css';
import Dropdown from './Dropdown';
import { AppBar, List, ListItem, Toolbar, useScrollTrigger } from '@mui/material';

const Nouns = [
  {
    title: '1+2 Nouns',
    path: '/1+2-Nouns',
    cName: 'dropdown-link'
  },
  {
    title: '2+1 Nouns',
    path: '/2+1-Nouns',
    cName: 'dropdown-link'
  },
  {
    title: '2+2 Nouns',
    path: '/2+2-Nouns',
    cName: 'dropdown-link'
  },
  {
    title: 'Chinese-originated',
    path: '/chinese-originated',
    cName: 'dropdown-link'
  },
  {
    title: 'Compound Nouns',
    path: '/compounds',
    cName: 'dropdown-link'
  },
  {
    title: 'Gairaigo',
    path: '/gairaigo',
    cName: 'dropdown-link'
  }
];

const Verbs = [
  {
    title: 'Dictionary Form',
    path: '/dictionary',
    cName: 'dropdown-link'
  },
  {
    title: 'ます form',
    path: '/masu-form',
    cName: 'dropdown-link'
  },
  {
    title: 'Dictionary Negative Conjugations',
    path: '/negatives',
    cName: 'dropdown-link'
  },
  {
    title: 'て・た Form',
    path: '/te-ta',
    cName: 'dropdown-link'
  }
];


function ElevationScroll(props) {
  const { children } = props;
  const trigger = useScrollTrigger({
    disableHysteresis: true,
    threshold: 0,
  });

  return React.cloneElement(children, {
    elevation: trigger ? 4 : 0,
  });
}


function Navbar() {
  const [nounDropdown, setNounDropdown] = useState(false);
  const [verbDropdown, setVerbDropdown] = useState(false);

  const nounEnter = () => {
    if (window.innerWidth < 960) {
      setNounDropdown(false);
    } else {
      setNounDropdown(true);
    }
  };

  const nounLeave = () => {
    if (window.innerWidth < 960) {
      setNounDropdown(false);
    } else {
      setNounDropdown(false);
    }
  };

  const verbEnter = () => {
    if (window.innerWidth < 960) {
      setVerbDropdown(false);
    } else {
      setVerbDropdown(true);
    }
  };

  const verbLeave = () => {
    if (window.innerWidth < 960) {
      setVerbDropdown(false);
    } else {
      setVerbDropdown(false);
    }
  };

  return (
    <ElevationScroll>
      <AppBar className='navbar' position='sticky'>
        <Toolbar>
          <Link to='/' className='navbar-logo'>
            JPP
          </Link>
          <List className={'nav-menu'}>
            <ListItem
              className='nav-item'
              onMouseEnter={nounEnter}
              onMouseLeave={nounLeave}
            >
              <Link
                to='/nouns'
                className='nav-links'
              >
                Nouns
              </Link>
              {nounDropdown && <Dropdown MenuItems={ Nouns }/>}
            </ListItem>
            <ListItem
              className='nav-item'
              onMouseEnter={verbEnter}
              onMouseLeave={verbLeave}
            >
              <Link
                to='/verbs'
                className='nav-links'
              >
                Verbs
              </Link>
              {verbDropdown && <Dropdown MenuItems={ Verbs }/>}
            </ListItem>
            <ListItem className='nav-item'>
              <Link
                to='/names'
                className='nav-links'
              >
                Names
              </Link>
            </ListItem>
            <ListItem className='nav-item'>
              <Link
                to='/generic_pitch_tips'
                className='nav-links'
              >
                Generic Pitch Accents
              </Link>
            </ListItem>
          </List>
        </Toolbar>
      </AppBar>
    </ElevationScroll>
  );
}

export default Navbar;
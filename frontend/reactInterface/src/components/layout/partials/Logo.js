import React from 'react';
import classNames from 'classnames';
import { Link } from 'react-router-dom';
import Image from '../../elements/Image';

const Logo = ({
  className,
  ...props
}) => {

  const classes = classNames(
    'brand',
    className
  );

  return (
    <div
      {...props}
      className={classes}
    >
      <h2 className="m-0">
        <Link to="/">
          <Image
            src={require('./../../../assets/images/logo.svg')}
            alt="Open"
            width={270}
            height={270}/>
        </Link>
      </h2>
    </div>
  );
}

export default Logo;
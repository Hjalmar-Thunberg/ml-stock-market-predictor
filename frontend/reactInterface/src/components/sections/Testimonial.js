import React from 'react';
import classNames from 'classnames';
import { SectionTilesProps } from '../../utils/SectionProps';
import SectionHeader from './partials/SectionHeader';
import Kardo from '../../assets/images/kardo.png'
// import Chris from '../../assets/images/chris.png'
// import Hugo from '../../assets/images/hugo.png'
// import Hjalmar from '../../assets/images/hjalmar.png'

const propTypes = {
  ...SectionTilesProps.types
}

const defaultProps = {
  ...SectionTilesProps.defaults
}

const Testimonial = ({
  className,
  topOuterDivider,
  bottomOuterDivider,
  topDivider,
  bottomDivider,
  hasBgColor,
  invertColor,
  pushLeft,
  ...props
}) => {

  const outerClasses = classNames(
    'testimonial section',
    topOuterDivider && 'has-top-divider',
    bottomOuterDivider && 'has-bottom-divider',
    hasBgColor && 'has-bg-color',
    invertColor && 'invert-color',
    className
  );

  const innerClasses = classNames(
    'testimonial-inner section-inner',
    topDivider && 'has-top-divider',
    bottomDivider && 'has-bottom-divider'
  );

  const tilesClasses = classNames(
    'tiles-wrap',
    pushLeft && 'push-left'
  );

  const sectionHeader = {
    title: 'Developers',
    paragraph: ''
  };

  return (
    <section
      {...props}
      className={outerClasses}
    >
      <div className="container">
        <div className={innerClasses}>
          <SectionHeader data={sectionHeader} className="center-content" />
          <div className={tilesClasses}>

          <div className="tiles-item reveal-from-left" data-reveal-delay="200">
              <div className="tiles-item-inner">
              <img src={Kardo} alt="" />
                <div className="testimonial-item-content">
                <p>Lorem Ipsum</p>
                </div>
                <div className="testimonial-item-footer text-xs mt-32 mb-0 has-top-divider">
                  <span className="testimonial-item-link">
                    <a>Hjalmar Thunberg</a>
                  </span>
                  <span className="text-color-low"> - </span>
                  <span className="testimonial-item-name text-color-high"></span>
                </div>
              </div>
            </div>

            <div className="tiles-item reveal-from-left" data-reveal-delay="200">
              <div className="tiles-item-inner">
              <img src={Kardo} alt="" />
                <div className="testimonial-item-content">
                  <p>Lorem Ipsum</p>
               
                </div>
                <div className="testimonial-item-footer text-xs mt-32 mb-0 has-top-divider">
                  <span className="testimonial-item-link">
                    <a>Christian O'Neill </a>
                  </span>
                  <span className="text-color-low"> - </span>
                  <span className="testimonial-item-name text-color-high"></span>
                </div>
              </div>
            </div>

            <div className="tiles-item reveal-from-left" data-reveal-delay="200">
              <div className="tiles-item-inner">
              <img src={Kardo} alt="" />
                <div className="testimonial-item-content">
                <p>Lorem Ipsum</p>
                </div>
                <div className="testimonial-item-footer text-xs mt-32 mb-0 has-top-divider">
                  <span className="testimonial-item-link">
                    <a>Kardo Marof</a>
                  </span>
                  <span className="text-color-low"> - </span>
                  <span className="testimonial-item-name text-color-high"></span>
                </div>
              </div>
            </div>

            <div className="tiles-item reveal-from-left" data-reveal-delay="200">
              <div className="tiles-item-inner">
              <img src={Kardo} alt="" />
                <div className="testimonial-item-content">
                <p>Lorem Ipsum</p>
                </div>
                <div className="testimonial-item-footer text-xs mt-32 mb-0 has-top-divider">
                  <span className="testimonial-item-link">
                    <a>Hugo Hempel</a>
                  </span>
                  <span className="text-color-low"> - </span>
                  <span className="testimonial-item-name text-color-high"></span>
                </div>
              </div>
            </div>

          </div>
        </div>
      </div>
    </section>
  );
}

Testimonial.propTypes = propTypes;
Testimonial.defaultProps = defaultProps;

export default Testimonial;
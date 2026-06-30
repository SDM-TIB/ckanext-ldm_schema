(function () {
  'use strict';

  function openSectionsWithErrors() {
    var errorFields = document.querySelectorAll(
      '.scheming-section .error, .scheming-section .has-error'
    );

    var firstOpenedSection = null;

    errorFields.forEach(function (errorEl) {
      var section = errorEl.closest('details.scheming-section');
      if (section && !section.open) {
        section.open = true;
        if (!firstOpenedSection) {
          firstOpenedSection = section;
        }
      }
    });

    if (firstOpenedSection) {
      firstOpenedSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  }

  document.addEventListener('DOMContentLoaded', openSectionsWithErrors);
})();

(function () {
  'use strict';

  var ANIMATION_DURATION = 250; // ms
  var ANIMATION_EASING = 'ease-out';

  function setupAnimatedDetails(details) {
    var summary = details.querySelector('summary');
    var content = details.querySelector('.scheming-section-body');

    if (!summary || !content) return;

    details._animating = false;  // track whether an animation is currently running, to avoid overlap

    summary.addEventListener('click', function (event) {
      event.preventDefault();

      if (details._animating) return;

      if (details.open) {
        shrink(details, content);
      } else {
        grow(details, content);
      }
    });
  }

  function grow(details, content) {
    details.style.overflow = 'hidden';
    details.open = true; // must open immediately so content has real height to measure

    var startHeight = '0px';
    var endHeight = content.offsetHeight + 'px';

    details._animating = true;

    var animation = details.animate(
      { height: [startHeight, endHeight] },
      { duration: ANIMATION_DURATION, easing: ANIMATION_EASING }
    );

    animation.onfinish = function () {
      details._animating = false;
      details.style.overflow = '';
      details.style.height = '';
    };
  }

  function shrink(details, content) {
    details.style.overflow = 'hidden';

    var startHeight = details.offsetHeight + 'px';
    var endHeight = (details.offsetHeight - content.offsetHeight) + 'px';

    details._animating = true;

    var animation = details.animate(
      { height: [startHeight, endHeight] },
      { duration: ANIMATION_DURATION, easing: ANIMATION_EASING }
    );

    animation.onfinish = function () {
      details.open = false; // close only after the shrink animation completes
      details._animating = false;
      details.style.overflow = '';
      details.style.height = '';
    };
  }

  document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('details.scheming-section').forEach(setupAnimatedDetails);
  });
})();



/**
 * Animation dispenser.
 *
 * Set up a new const animationName = new Animation(target,animation,autoClear,callback);
 * To add an animation to a div.
 *
 * @param target {Element} : This is the target you want to apply the animation to.
 * @param animation {String} : The name of the animation you want to use (found in Animations.scss).
 * @param autoClear {Boolean} : True if you want the logic to remove the class when the animation is done.
 * 								False when doing it manually by calling animationName.stop();
 * @param callback {Function} : The callback function for when the animation has completed and the class has been removed again.
 * @constructor
 */
const Animator = function(target: Element, animation: string, autoClear: boolean, callback: Function){

	const self = this;

	// Check if target & animation are filled provided.
	if(!target){

		console.warn('Animation: No target element found', target);
		return;
	}

	if(!animation){

		console.warn('Animation: No valid animation provided',animation);
		return;
	}

	// Attach the animation class.
	target.classList.add(animation);

	// If autoClear is true we add an EventListener to remove the class once the animation is done.
	if(autoClear){

		target.addEventListener('animationend', clearAnimation);
	}

	// The function that clears the animation and eventListener.
	function clearAnimation(){

		self.stop();
		target.removeEventListener('animationend', clearAnimation);
	}

	// Remove the class and fire the callback if there is one. Can be called manually.
	this.stop = function(){

		target.classList.remove(animation);

		// Fire a callback
		if(callback && typeof callback === 'function'){

			callback();
		}
	};
};
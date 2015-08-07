Common Angular Utilities
========================

Install with Bower.

## Provides:

1. Passive Messenger
2. Modals
3. PubSub
4. Loading

## Usage:

### Passive Messenger

Add `cs.passive-messenger` to your module's list of dependencies

Provides passive messages ala GMail.

To use, include an element like so inside of your `<body>` tag:

```
#!html

<div x-passive-messenger></div>
```

Then, in your controller/service, use the `passive_messenger` service:

```
#!javascript

passive_messenger.info('Hello!', 'Say Hi Back', say_hi_callback);
```

Available methods are `info`, `success`, `warning`, and `error`

### Modal

Add `cs.modal` to your module's list of dependencies; needs the `pubsub` service (`cs.pubsub`) injected on your controller/service as well

Built on top of [Twitter Bootstrap Modal](http://getbootstrap.com/javascript/#modals), this provides AngularJS-powered modal windows.

Your modal should follow the same markup as Bootstrap's and should include the `modal` directive as attribute on your `.modal` element.

Show modals by using `cs.pubsub`:

```
#!javascript

pubsub.publish('modal:modalName:show', model, callback, _hide_callback);
```

..wherein `modalName` is your modal's `id`, or the value of the `modal` attribute.

It's advisable to have your modal get its own controller as the `modal` directive binds several properties to its parent `$scope`.

In its controller, you can...

* access the passed model and callback through `$scope.model` and `$scope.callback`
* execute code when showing the modal by defining the function `$scope.on_show`
* hide/(re)show the modal with `$scope.modal.hide()` and `$scope.modal.show()`

### PubSub

Add `cs.pubsub` to your module's list of dependencies

More or less blatantly taken from [here](https://github.com/phiggins42/bloody-jquery-plugins/blob/master/pubsub.js).

### Loading

Add `cs.loading` to your module's list of dependencies

Provides a service and directive of the same name (`loading`) and works in pair. Useful for showing "loaders" that depends on AngularJS' promises.

The best way to show this is through an example:

```
#!html

<div class="loader" loading="loading_in_progress">
  <span class="loading-spinner"></span>
  <p>Avengers loading...</p>
</div>
```

```
#!javascript

$scope.loading_in_progress = loading.new();
$scope.loading_in_progress.watch($http.get("/api/avengers"));
```

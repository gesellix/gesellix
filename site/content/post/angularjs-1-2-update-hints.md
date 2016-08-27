
+++
date = "2013-11-27"
draft = false
title = "AngularJS 1.2 update hints"
slug = "angularjs-1-2-update-hints"
tags = ['angularjs', 'migration', 'update', 'directive', 'test', 'phantomjs']
banner = ""
aliases = ['/angularjs-1-2-update-hints/']
+++

As you might have noticed, [AngularJS](http://angularjs.org/) <s>1.2.2</s> 1.2.3 has been released lately, [without dedicated announcement](http://blog.angularjs.org/2013/11/on-launching-angular-12-what-we-learned.html). Our update from an AngularJS 1.2-rc2 has been quite smooth, only two hints might be noteable in addition to the official [migration guide](http://docs.angularjs.org/guide/migration).

1. With the current version the AngularJS team has fixed some issues regarding the isolate scope as described in the changelog for the 1.2.0 release or at the relevant GitHub issues [#1924](https://github.com/angular/angular.js/issues/1924) and [#2500](https://github.com/angular/angular.js/issues/2500).
In directive tests you might currently use the isolate scope of an element using the notion `element.scope()`. With the current release you have to use the newly introduced function `element.isolateScope()`. Just a simple find and replace task :-)

2. Don't forget to check third party libraries for compatibility updates. We used the [Angular-UI Select2 directive](https://github.com/angular-ui/ui-select2) in an older release 0.0.2. Running our e2e-tests produced some strange and non-deterministic error messages in PhantomJS, but not in Chrome or other standard browsers. The errors seemed to be triggered due to directive priority changes in Angular 1.2.0, so the update to the current release 0.0.4 of ui-select2 made the errors go away by [setting a fixed priority](https://github.com/angular-ui/ui-select2/commit/6b20bd783a4f7cf5f87c01f9ffb34635477ce425).



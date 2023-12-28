
+++
date = "2012-08-12"
draft = false
title = "Modularization of the Fest Assertions library"
slug = "modularization-of-the-fest-assertions-library"
tags = ['gesellix.de', 'fest assert', 'modularization']
banner = ""
aliases = ['/modularization-of-the-fest-assertions-library/']
+++

<p>The <a href="http://fest.easytesting.org/" target="_blank">Fest Assertions</a> library, a fluent Java API for writing assertions in your test or production code, is quite popular in my development team. Because of it's clean and fluent interface, it was no question to me when trying to use it in an <a href="http://developer.android.com/index.html" target="_blank">Android</a> project. But due to it's dependency on java.awt classes and due to Android's missing support for them, I currently cannot use it for writing tests in my Android codebase.</p>
<p>There might be several solutions to solve such an incompatibility, like adding classes providing missing packages in Android. Another solution is breaking the fest assertions library into several modules, so that one can use only Android compatible fest assertion modules. The library fest-assert is currently being <a href="https://github.com/alexruiz/fest-assert-2.x" target="_blank">refactored at GitHub</a>, so nothing hinders us from forking and giving modularization a chance.</p>
<p>The whole approach is quite easy:</p>
<ul>
<li>identify all awt dependent classes and corresponding resources in artifact A and move them to another artifact B.</li>
<li>for all commonly used classes between artifacts A and B, move them to a third artifact C, so that both A and B can be dependent on C.</li>
<li>in order to ease dependency management for users, create another artifact X, which itself depends on A and B.</li>
</ul>
<p>Usually, most users should only depend on artifact X, which gives them most of the commonly used assertions. For special needs, you just drop your dependency on artifact X and replace it with one or more of the smaller modules. Using the example above, we have the following modules available:<br /><strong>A</strong>: fest-assert-core (<a href="https://github.com/gesellix/fest-assert-2.x" target="_blank">https://github.com/gesellix/fest-assert-2.x</a>): contains all core assertions, abstract base classes and the main API, but without dependencies on java.awt classes.<br /><strong>B</strong>: fest-assert-awt (<a href="https://github.com/gesellix/fest-assert-awt-2.x" target="_blank">https://github.com/gesellix/fest-assert-awt-2.x</a>): contains all awt assertions, which have simply been moved from the old core assertion library.<br /><strong>C</strong>: fest-test (<a href="https://github.com/gesellix/fest-test" target="_blank">https://github.com/gesellix/fest-test</a>): contains commonly used test classes. Some classes have been moved from the fest-assert-core artifact, to make them available for fest-assert-awt, too.<br /><strong>X</strong>: fest-assert (<a href="https://github.com/gesellix/fest-assert" target="_blank">https://github.com/gesellix/fest-assert</a>): A minimal artifact without Java classes, providing only dependencies on both fest-assert-core and fest-assert-awt. This artifact should be used in most cases, so that fest developers could continue modularization of fest-assert-core without breaking any client code. fest-assert should be used as facade to all commonly used assertion artifacts.</p>
<p>The only breaking change is a new factory class for the new awt specific artifact, in this case you would use "AwtAssertions" instead of "Assertions". You can find an example using both artifacts in on test class in the <a href="https://github.com/gesellix/fest-examples" target="_blank">fest-examples</a> repository (see the class <a href="https://github.com/gesellix/fest-examples/blob/master/src/main/java/org/fest/assertions/examples/MixedAssertionFactoriesTest.java" target="_blank">MixedAssertionFactoriesTest</a>). The whole modularized code can be found at the provided links, a discussion about this approach can be found at the fest <a href="https://groups.google.com/d/topic/easytesting-dev/qVI2n2GGB44/discussion" target="_blank">easytesting developer group</a>.</p>
<p>After discussion, I hope all changes find their way into the main repository at <a href="https://github.com/alexruiz/" target="_blank">https://github.com/alexruiz/</a> and further modularization will take place to make Fest Assertions compatible with GWT and other frameworks. In case you want to support or improve this approach, please provide feedback at the google group or at GitHub!</p>


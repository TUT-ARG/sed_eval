.. _sound_event:

Sound Event Detection
=====================

The task of sound event detection involves locating and classifying
sounds in audio recordings - estimating onset and offset for distinct
sound event instances and providing a textual descriptor for each. The
usual approach for this problem is supervised learning with sound event
classes defined in advance.

Metrics are defined for polyphonic sound event detection, in which the
ground truth and system output contain overlapping sound event instances.

Two types of metrics are implemented:

- **segment-based metrics**  - the ground truth and system output are compared in a fixed time grid; sound events are marked as active or inactive in each segment;
- **event-based metrics** - the ground truth and system output are compared at event instance level;

Intermediate statistics
-----------------------

Segment-based
^^^^^^^^^^^^^

- *true positive*: the ground truth and system output both indicate an event to be active in that segment
- *false positive*: the ground truth indicates an event to be inactive in that segment, but the system output indicates it as active
- *false negative*: the ground truth indicates an event to be active in that segment, but the system output indicates it as inactive.
- *true negative*: the ground truth and system output both indicate an event to be inactive.

Segment-based metrics implementation allow selecting the desired segment length for evaluation (see ``time_resolution`` parameter).

Event-based
^^^^^^^^^^^

- *true positive*: an event in the system output that has a temporal position overlapping with the temporal position of an event with the same label in the ground truth. A *collar* is usually allowed for the onset and offset, or a tolerance with respect to the ground truth event duration.
- *false positive*: an event in the system output that has no correspondence to an event with same label in the ground truth within the allowed tolerance;
- *false negative*: an event in the ground truth that has no correspondence to an event with same label in the system output within the allowed tolerance.
- *true negative*: event-based metrics have no meaningful true negatives.

Event-based metrics implementation allow selecting the desired collar size (see ``t_collar`` parameter) and use of onset only or onset and offset conditions for evaluation (see ``evaluate_onset`` and ``evaluate_offset`` parameters).

.. _averaging:

Averaging
^^^^^^^^^



**Micro-averaging** - intermediate statistics are aggregated over all test
data, then metrics are calculated; each instance has equal influence on
the final metric value;

**Macro-averaging** - intermediate statistics are aggregated class-wise,
class-based metrics are calculated, then average of class based metrics;
each class has equal influence on the final metric value.

Micro and macro averages can result in very different values when
classes are highly unbalanced or performance on individual classes is
very different.

Cross-validation
^^^^^^^^^^^^^^^^

Recommended calculation for a cross-validation setup is to run all
train/test folds and perform evaluation at the end (no fold-wise
evaluation!).
The reason is that folds are most often unbalanced due to the multilabel
nature of the problem, and this results in biases when averaging. For
more details, consult [1]_.


Implemented metrics
-------------------

Precision, Recall and F-score
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. math::

    P=\frac{TP}{TP+FP},\quad R=\frac{TP}{TP+FN},\quad F=\frac{2 \cdot P \cdot R}{P+R}


These can be calculated segment based or event based, micro or macro averaged.

Sensitivity and specificity
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. math::
    Sensitivity = \frac{TP}{TP+FN},\quad
    Specificity = \frac{TN}{TN+FP}

Accuracy
^^^^^^^^

.. math::
    accuracy = \frac{TP+TN}{TP+TN+FP+FN}

.. math::
    accuracy2 = \frac{TP}{TP+FP+FN}

Balanced accuracy
^^^^^^^^^^^^^^^^^

.. math::
    BACC = factor \cdot \frac{TP}{TP+FN} +(1-factor) \cdot \frac{TN}{TN+FP}

Specificity and accuracy variants are only calculated as segment-based
metrics.


Error Rate
^^^^^^^^^^

**Segment-based**

**Substitutions** in segment *k* - *S(k)* - the number of ground truth events
for which a correct event was not output, yet something else was. One
substitution is equivalent to having one false positives and one false
negatives in the same segment. There is no need to designate which
erroneous event substitutes which.

**Insertions** in segment *k* - *I(k)* - events in system output that are not
correct (false positives after substitutions are accounted for).

**Deletions** in segment *k* - *D(k)* - events in ground truth that are not
correct (false positives after substitutions are accounted for).

.. math::
    &S(k) = min(FN(k),FP(k)) \nonumber \\
    &D(k) = max(0,FN(k)-FP(k)) \\
    &I(k)= max(0,FP(k)-FN(k)) \nonumber

.. math::
    ER=\frac{\sum_{k=1}^K{S(k)}+\sum_{k=1}^K{D(k)}+\sum_{k=1}^K{I(k)}}{\sum_{k=1}^K{N(k)}}

*N(k)* is the number of events in segment *k* in ground truth.

**Event-based**

**Substitutions** - events in system output with correct temporal position
but incorrect class label

**Insertions** - events in system output unaccounted for as correct or
substituted

**Deletions** - events in ground truth unaccounted for as correct or substituted

.. math::
    ER=\frac{S + D + I}{N}

*N* is the total number of events in ground truth.

Code
----

.. automodule:: sed_eval.sound_event

Rerefences
----------

.. [1] Forman, G. and Scholz, M.
       "Apples-to-Apples in Cross-Validation Studies: Pitfalls in Classifier Performance Measurement".
       SIGKDD Explor. Newsl. 12, 1, November 2010, pp. 49-57.
       http://kdd.org/exploration_files/v12-1-p49-forman-sigkdd.pdf
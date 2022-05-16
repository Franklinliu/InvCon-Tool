package daikon.inv.binary.sequenceScalar;

import daikon.Global;
import daikon.PptSlice;
import daikon.VarInfo;
import daikon.derive.binary.SequenceFloatSubscript;
import daikon.derive.binary.SequenceFloatSubsequence;
import daikon.derive.ternary.SequenceFloatArbitrarySubsequence;
import daikon.derive.unary.SequenceInitialFloat;
import daikon.derive.unary.SequenceMax;
import daikon.derive.unary.SequenceMin;
import daikon.inv.*;
import daikon.inv.binary.twoSequence.SubSequenceFloat;
import org.checkerframework.checker.interning.qual.Interned;
import org.checkerframework.checker.lock.qual.GuardSatisfied;
import org.checkerframework.checker.nullness.qual.Nullable;
import org.checkerframework.dataflow.qual.Pure;
import org.checkerframework.dataflow.qual.SideEffectFree;
import org.plumelib.util.Pair;
import typequals.prototype.qual.NonPrototype;
import typequals.prototype.qual.Prototype;

import java.util.Arrays;
import java.util.logging.Level;
import java.util.logging.Logger;

public class InfConMsgValueMember extends SequenceFloat{

    // We are Serializable, so we specify a version to allow changes to
    // method signatures without breaking serialization.  If you add or
    // remove fields, you should change this number to the current date.
    static final long serialVersionUID = 20210127L;

    public static final Logger debug = Logger.getLogger("daikon.inv.binary.InfConMsgValueMember");

    // Variables starting with dkconfig_ should only be set via the
    // daikon.config.Configuration interface.
    /** Boolean. True iff Member invariants should be considered. */
    public static boolean dkconfig_enabled = Invariant.invariantEnabledDefault;

    InfConMsgValueMember(PptSlice ppt) {
        super(ppt);
    }

    @Prototype InfConMsgValueMember() {
        super();
    }

    private static @Prototype InfConMsgValueMember proto = new @Prototype InfConMsgValueMember();

    /** Returns the prototype invariant for MemberFloat */
    public static @Prototype InfConMsgValueMember get_proto() {
        return proto;
    }


    /**
     * This method computes the confidence that this invariant occurred by chance. Clients should call
     * {@link #getConfidence()} instead.
     *
     * <p>This method need not check the value of field "falsified", as the caller does that.
     *
     * @return confidence of this invariant
     * @see #getConfidence()
     */
    @Override
    protected double computeConfidence() {
        return Invariant.CONFIDENCE_JUSTIFIED;
    }

    /**
     * Return a printed representation of this invariant, in the given format.
     *
     * @param format
     */
    @SideEffectFree
    @Override
    public String format_using(@GuardSatisfied InfConMsgValueMember this, OutputFormat format) {

        if (format.isJavaFamily()) {
            return format_java_family(format);
        }
        if (format == OutputFormat.DAIKON) {
            return format_daikon();
        } else if (format == OutputFormat.ESCJAVA) {
            return format_esc();
        } else if (format == OutputFormat.CSHARPCONTRACT) {
            return format_csharp_contract();
        } else {
            return format_unimplemented(format);
        }
    }

    /**
     * Returns true iff the two invariants represent the same mathematical formula. Does not consider
     * the context such as variable names, confidences, sample counts, value counts, or related
     * quantities. As a rule of thumb, if two invariants format the same, this method returns true.
     * Furthermore, in many cases, if an invariant does not involve computed constants (as "x&gt;c"
     * and "y=ax+b" do for constants a, b, and c), then this method vacuously returns true.
     *
     * @param other the invariant to compare to this one
     * @return true iff the two invariants represent the same mathematical formula. Does not consider
     * @throws RuntimeException if other.getClass() != this.getClass()
     */
    @Override
    public boolean isSameFormula(Invariant other) {
        assert other instanceof InfConMsgValueMember;
        return true;
    }

    /**
     * Instantiates (creates) an invariant of the same class on the specified slice. Must be
     * overridden in each class. Must be used rather than {@link #clone} so that checks in {@link
     * #instantiate} for reasonable invariants are done.
     *
     * <p>The implementation of this method is almost always {@code return new
     * <em>InvName</em>(slice);}
     *
     * @param slice
     * @return the new invariant
     */
    @Override
    protected @NonPrototype Invariant instantiate_dyn(PptSlice slice) {
        return new InfConMsgValueMember(slice);
    }

    /**
     * Returns whether or not this class of invariants is currently enabled.
     *
     * <p>Its implementation is almost always {@code return dkconfig_enabled;}.
     */
    @Override
    public boolean enabled() {
        return dkconfig_enabled;
    }


    public String format_daikon(@GuardSatisfied InfConMsgValueMember this) {
        String sclname = sclvar().name();
        String seqname = seqvar().name();
        return "<MSG.VALUE IsMember> "+ sclname + " in " + seqname;
    }

    public String format_java() {
        return "( (daikon.inv.FormatJavaHelper.memberOf("
                + sclvar().name()
                + " , "
                + seqvar().name()
                + " ) == true ) ";
    }

    public String format_java_family(@GuardSatisfied InfConMsgValueMember this, OutputFormat format) {
        String sclname = sclvar().name_using(format);
        String seqname = seqvar().name_using(format);
        return "daikon.Quant.memberOf(" + sclname + " , " + seqname + " )";
    }

    public String format_esc(@GuardSatisfied InfConMsgValueMember this) {
        // "exists x in a..b : P(x)" gets written as "!(forall x in a..b : !P(x))"
        String[] form = VarInfo.esc_quantify(seqvar(), sclvar());
        return "!" + form[0] + "(" + form[1] + " != " + form[2] + ")" + form[3];
    }

    public String format_csharp_contract(@GuardSatisfied InfConMsgValueMember this) {
        String sclname = sclvar().csharp_name();
        String[] split = seqvar().csharp_array_split();
        return "Contract.Exists(" + split[0] + ", x => x" + split[1] + ".Equals(" + sclname + "))";
    }

    /**
     * Presents a sample to the invariant. Returns whether the sample is consistent with the
     * invariant. Does not change the state of the invariant.
     *
     * @param v1
     * @param v2
     * @param count how many identical samples were observed in a row. For example, three calls to
     *              check_modified with a count parameter of 1 is equivalent to one call to check_modified with
     *              a count parameter of 3.
     * @return whether or not the sample is consistent with the invariant
     */
    @Override
    public InvariantStatus check_modified(double @Interned [] v1, double v2, int count) {
//        debug.log(Level.WARNING, format() + " " + v2 + " and " + Arrays.toString(v1) + sclvar().str_name() + " "+seqvar().str_name());
        if (sclvar().str_name().equals("msg.value") || sclvar().str_name().equals("orig(msg.value)") ){
            debug.log(Level.INFO, format() + " " + v2 + " and " + Arrays.toString(v1));
                if (v1 == null) {
                    return InvariantStatus.FALSIFIED;
                }
                else if (Global.fuzzy.indexOf(v1, v2) == -1) {
                    return InvariantStatus.FALSIFIED;
                }
                return InvariantStatus.NO_CHANGE;
        }else{
            return InvariantStatus.FALSIFIED;
        }
    }

    /**
     * Similar to {@link #check_modified} except that it can change the state of the invariant if
     * necessary. If the invariant doesn't have any state, then the implementation should simply call
     * {@link #check_modified}. This method need not check for falsification; that is done by the
     * caller.
     *
     * @param v1
     * @param v2
     * @param count
     */
    @Override
    public InvariantStatus add_modified(double @Interned [] v1, double v2, int count) {
        InvariantStatus is = check_modified(v1, v2, count);
        if (debug.isLoggable(Level.FINE) && (is == InvariantStatus.FALSIFIED)) {
            debug.fine(
                    "Member destroyed:  " + format() + " because " + v2 + " not in " + Arrays.toString(v1));
        }
        return is;
    }


    @Pure
    @Override
    public @Nullable DiscardInfo isObviousStatically(VarInfo[] vis) {
        if (isObviousMember(sclvar(vis), seqvar(vis))) {
            log("scalar is obvious member of");
            return new DiscardInfo(
                    this,
                    DiscardCode.obvious,
                    sclvar().name() + " is an obvious member of " + seqvar().name());
        }
        return super.isObviousStatically(vis);
    }

    /** Check whether sclvar is a member of seqvar can be determined statically. */
    @Pure
    public static boolean isObviousMember(VarInfo sclvar, VarInfo seqvar) {

        VarInfo sclvar_seq = sclvar.isDerivedSequenceMember();

        if (sclvar_seq == null) {
            // The scalar is not obviously (lexically) a member of any array.
            return false;
        }
        // isObviousImplied: a[i] in a; max(a) in a
        if (sclvar_seq == seqvar) {
            // The scalar is a member of the same array.
            return true;
        }
        // The scalar is a member of a different array than the sequence.
        // But maybe the relationship is still obvious, so keep checking.

        // isObviousImplied: when b==a[0..i]:  b[j] in a; max(b) in a
        // If the scalar is a member of a subsequence of the sequence, then
        // the scalar is a member of the full sequence.
        // This is satisfied, for instance, when determining that
        // max(B[0..I]) is an obvious member of B.
        VarInfo sclseqsuper = sclvar_seq.isDerivedSubSequenceOf();
        if (sclseqsuper == seqvar) {
            return true;
        }

        // We know the scalar was derived from some array, but not from the
        // sequence variable.  If also not from what the sequence variable was
        // derived from, we don't know anything about membership.
        // Check:
        //  * whether comparing B[I] to B[0..J]
        //  * whether comparing min(B[0..I]) to B[0..J]
        VarInfo seqvar_super = seqvar.isDerivedSubSequenceOf();
        if ((seqvar_super != sclvar_seq) && (seqvar_super != sclseqsuper)) {
            return false;
        }

        // If the scalar is a positional element of the sequence from which
        // the sequence at hand was derived, then any relationship will be
        // (mostly) obvious by comparing the length of the sequence to the
        // index.  By contrast, if the scalar is max(...) or min(...), all bets
        // are off.
        if (seqvar.derived instanceof SequenceFloatSubsequence
                || seqvar.derived instanceof SequenceFloatArbitrarySubsequence) {

            // Determine the left index/shift and right index/shift of the
            // subsequence.  If the left VarInfo is null, the sequence starts
            // at the beginning.  If the right VarInfo is null, the sequence stops
            // at the end.
            VarInfo seq_left_index = null;
            VarInfo seq_right_index = null;
            int seq_left_shift = 0, seq_right_shift = 0;
            if (seqvar.derived instanceof SequenceFloatSubsequence) {
                // the sequence is B[0..J-1] or similar.  Get information about it.
                SequenceFloatSubsequence seqsss = (SequenceFloatSubsequence) seqvar.derived;
                if (seqsss.from_start) {
                    seq_right_index = seqsss.sclvar();
                    seq_right_shift = seqsss.index_shift;
                } else {
                    seq_left_index = seqsss.sclvar();
                    seq_left_shift = seqsss.index_shift;
                }
            } else if (seqvar.derived instanceof SequenceFloatArbitrarySubsequence) {
                // the sequence is B[I+1..J] or similar
                SequenceFloatArbitrarySubsequence ssass = (SequenceFloatArbitrarySubsequence) seqvar.derived;
                seq_left_index = ssass.startvar();
                seq_left_shift = (ssass.left_closed ? 0 : 1);
                seq_right_index = ssass.endvar();
                seq_right_shift = (ssass.right_closed ? 0 : -1);
            } else {
                throw new Error();
            }

            // if the scalar is a a subscript (b[i])
            if (sclvar.derived instanceof SequenceFloatSubscript) {

                SequenceFloatSubscript sclsss = (SequenceFloatSubscript) sclvar.derived;
                VarInfo scl_index = sclsss.sclvar(); // "I" in "B[I]"
                int scl_shift = sclsss.index_shift;

                // determine if the scalar index is statically included in the
                // left/right sequence
                boolean left_included = false, right_included = false;
                if (seq_left_index == null) {
                    left_included = true;
                }
                if (seq_left_index == scl_index) {
                    if (seq_left_shift <= scl_shift) left_included = true;
                }
                if (seq_right_index == null) {
                    right_included = true;
                }
                if (seq_right_index == scl_index) {
                    if (seq_right_shift >= scl_shift) right_included = true;
                }
                if (left_included && right_included) {
                    return true;
                }

                // else if the scalar is a specific positional element (eg, b[0])
            } else if (sclvar.derived instanceof SequenceInitialFloat) {

                // isObviousImplied: B[0] in B[0..J]; also B[-1] in B[J..]
                SequenceInitialFloat sclse = (SequenceInitialFloat) sclvar.derived;
                int scl_index = sclse.index;
                if (((scl_index == 0) && seq_left_index == null)
                        || ((scl_index == -1) && seq_right_index == null))
                    // It might not be true, because the array could be empty;
                    // but if the array isn't empty, then it's obvious.  The empty
                    // array case is ok, because the variable itself would be
                    // destroyed in that case.
                    return true;

                // else if the scalar is min or max of a sequence
            } else if ((sclvar.derived instanceof SequenceMin)
                    || (sclvar.derived instanceof SequenceMax)) {
                Pair<DiscardCode, String> di = SubSequenceFloat.isObviousSubSequence(sclvar_seq, seqvar);
                return (di != null);
            }
        }

        return false;
    }

    @Override
    public String repr(@GuardSatisfied InfConMsgValueMember this) {
        return "Member" + varNames() + ": falsified=" + falsified;
    }
}

package daikon.derive.senary;

import daikon.ProglangType;
import daikon.VarInfo;
import daikon.derive.DerivationFactory;
import org.checkerframework.checker.nullness.qual.Nullable;

/** Factory to produce TernaryDerivations. */
public abstract class SenaryDerivationFactory implements DerivationFactory {

  /**
   * Create a set of derivations from three base variables. If the base variables aren't worth
   * deriving from, returns null.
   *
   * @param vi1 the first of the three base variables
   * @param vi2 the second of the three base variables
   * @param vi3 the third of the three base variables
   * @return a set of derivations based on three base variables. We allow more than one because the
   *     base variables may have multiple derived variables, per type of derivation. Can also be
   *     null if the variables have nothing to derive from.
   */
  public abstract SenaryDerivation @Nullable [] instantiate(VarInfo vi1, VarInfo vi2, VarInfo vi3, VarInfo vi4, VarInfo vi5, VarInfo vi6);

  // donot need to check type in this generic factory
  // delegate type checking in specific factory
  public static boolean checkType(VarInfo vi1) {
    if ((vi1.rep_type == ProglangType.DOUBLE_ARRAY) || (vi1.rep_type == ProglangType.BIGINT_ARRAY) || (vi1.rep_type == ProglangType.STRING_ARRAY) 
    || (vi1.rep_type == ProglangType.INT_ARRAY) || (vi1.rep_type == ProglangType.STRING)){
      return true;
    }else{
      return false;
    }
  }
  public static boolean checkType(VarInfo vi1, VarInfo vi2, VarInfo vi3) {
    if (!((vi1.rep_type == vi2.rep_type)  && (vi1.rep_type == vi3.rep_type)))
    {
      return true;
    }else{
      return false;
    }
  }
}
